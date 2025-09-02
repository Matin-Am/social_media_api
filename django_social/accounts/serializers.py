from rest_framework import serializers
from .models import  OtpCode
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True,label='Phone Number')
    email = serializers.EmailField(required=True,label = "Email Adress")
    password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True,label= "Confirm password")


    def validate(self, data ):
        p1 = data["password"]
        p2 = data["confirm_password"]
        if p1 and p2 and p1 != p2 :
            raise serializers.ValidationError("Passwords must match ! ")
        return data
        
    def validate_phone_number(self,value):
        phone_number = get_user_model().objects.filter(phone_number=value)
        if phone_number.exists():
            raise serializers.ValidationError("This phone number already exists ! ")
        return value
    
    def validate_email(self,value):
        email = get_user_model().objects.filter(email=value)
        if email.exists():
            raise serializers.ValidationError("This email already exists ! ")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8,write_only=True)


class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ("code",)
