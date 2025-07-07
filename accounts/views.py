from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import User , OtpCode
from utils import send_otp_code
from .sessions import Data
import random
# Create your views here.

class UserRegistrationAPI(APIView):
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
    