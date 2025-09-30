from django.shortcuts import render
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer,VerifyCodeSerializer,ChangePasswordSerializer,AuthTokenSerializer
from .models import User , OtpCode
from utils  import send_otp_code
from .sessions import Data
import random
# Create your views here.

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self,request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            data = Data(request,cd["phone_number"],cd["email"])
            data.save_data(cd["password"])
            random_code = random.randint(1111,9999)
            send_otp_code(cd["email"],random_code)
            OtpCode.objects.create(code=random_code,email=cd["email"])
            return Response({"Message":"We sent you a code , please check your email"},status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserVerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer
    def post(self,request):
        ser_data = VerifyCodeSerializer(data=request.data)
        session = request.session["user_data"]
        phone_number = list(session)[-1]
        if ser_data.is_valid():
            try:
                code_instance = OtpCode.objects.get(email=session[phone_number]["email"])
            except OtpCode.DoesNotExist:
                return  Response({"message":"No otp code for this email found"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if code_instance.is_expired():
                return Response({"message":"code is expired"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif code_instance.code != ser_data.validated_data["code"]:
                return Response({"mesaage":"Code is wrong,please try again"},status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(
                    phone_number = phone_number,
                    email = session[phone_number]["email"],
                    password = session[phone_number]["password"]
                )
                code_instance.delete()
                request.session.flush()
                return Response(UserRegistrationSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(ObtainAuthToken):
        serializer_class = AuthTokenSerializer
        def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token":token.key , 
                "email":user.phone_number ,
                "user_id":user.pk
            },status=status.HTTP_201_CREATED)

class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        request.user.auth_token.delete()
        return Response({"message":"Logged out successfully"},status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPIView(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def post(self,request):
        user = request.user
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        if not user.check_password(raw_password=ser_data.validated_data.get("old_password")):
            return Response({"Old password":"Wrong password !"},status=status.HTTP_400_BAD_REQUEST)
        try:
            password_validation.validate_password(
                password=ser_data.validated_data.get("new_password"),
                user=user)
        except ValidationError as e:
            return Response({"Error":e.messages},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(ser_data.validated_data.get("new_password"))
        user.save()
        return Response({"Message":"Password changed successfully"},status=status.HTTP_200_OK)