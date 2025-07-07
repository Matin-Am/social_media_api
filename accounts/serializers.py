from rest_framework import serializers




class UserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True,label='Phone Number')
    email = serializers.EmailField(required=True,label = "Email Adress")
    password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True,label= "Confirm password")

    