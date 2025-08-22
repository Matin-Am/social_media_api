from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import UserRegistrationSerializer , VerifyCodeSerializer
from .models import User , OtpCode
from utils  import send_otp_code
from .tasks import send_otp
from .sessions import Data
import random
# Create your views here.

class UserRegistrationAPI(APIView):
    """
    This api will send user an otp code throughout smtp email service
    """
    serializer_class = UserRegistrationSerializer
    def post(self,request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            data = Data(request,cd["phone_number"],cd["email"])
            data.save_data(cd["password"])
            random_code = random.randint(1111,9999)
            send_otp.apply_async(args=[cd["email"],random_code])
            OtpCode.objects.create(code=random_code,email=cd["email"])
            return Response({"Message":"We sent you a code , please check your email"},status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserVerifyCodeAPI(APIView):
    """
    This api will create a user in database when user verifies the code
    """
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
    
class UserLogoutAPI(APIView):
    authentication_classes = [TokenAuthentication,]
    def get(self,request,format=None):
        request.user.auth_token.delete()
        return Response({"message":"Logged out successfully"},status=status.HTTP_200_OK)
