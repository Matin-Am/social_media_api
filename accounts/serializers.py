from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import  OtpCode


class UserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True,label='Phone Number')
    email = serializers.EmailField(required=True,label = "Email Adress")
    password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True,label= "Confirm password")


    def validate(self, data ):
        p1 = data["password"]
        p2 = data["confirm_password"]
        if p1 and p2 and p1 != p2 :
            raise ValidationError("Passwords must match ! ")
        return data

class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ("code",)
