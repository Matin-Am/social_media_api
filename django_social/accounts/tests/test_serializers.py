from rest_framework.test import APITestCase
from ..serializers import UserRegistrationSerializer
from accounts.models import User


class TestUserRegistrationSerializer(APITestCase):

    def test_valid_data(self):
        """
        test if user sends valid data in serializers 
        """
        data = {"phone_number":"09121234567","email":"test@email.com","password":"test","confirm_password":"test"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 0)
        
    def test_invalid_data(self):
        """
        test if user sends invalid data in serializers 
        """
        data = {"phone_number":"09121234567","email":"invalid_email","password":"test","confirm_password":"test"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 1)
        self.assertEqual(list(serializer.errors.values())[0][0],'Enter a valid email address.')


    def test_empty_data(self):
        """
        test if user sends empty data in serializers 
        """
        data = {}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 4)

    def test_validate_unmatched_passwords(self):
        """
        test if user sends matched passwords in serializer
        """
        data = {"phone_number":"09121234567","email":"test@email.com","password":"test","confirm_password":"not_for_test"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 1)
        self.assertEqual(list(serializer.errors.values())[0][0],"Passwords must match !")

    def test_validate_phone_number(self):
        """
        test if user sends existed phone number
        """
        User.objects.create_user(phone_number='09551234567',email='test@email.com',password="test")
        data = {"phone_number":"09551234567","email":"test_app@email.com","password":"test","confirm_password":"test"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 1)
        self.assertEqual(list(serializer.errors.values())[0][0],"This phone number already exists !")

    def test_validate_email(self):
        """
        test if user sends existed phone number
        """
        User.objects.create_user(phone_number='09551234567',email='test@email.com',password="test")
        data = {"phone_number":"08991234567","email":"test@email.com","password":"test","confirm_password":"test"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors) , 1)
        self.assertEqual(list(serializer.errors.values())[0][0],"This email already exists !")