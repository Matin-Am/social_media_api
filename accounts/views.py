from django.shortcuts import render
from rest_framework.views import View
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import User
# Create your views here.

class UserRegistrationAPI(View):
    serializer_class = UserRegistrationSerializer
    def post(self,request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
           