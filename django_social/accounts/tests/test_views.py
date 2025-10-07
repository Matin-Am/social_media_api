from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from unittest.mock import patch
from ..models import OtpCode,User
from datetime import timedelta
from django.utils.timezone import now

class TestUserRegistrationAPIView(APITestCase):

    @patch("accounts.views.send_otp")
    def test_valid_data(self,mock_send_otp_code):
        """
        test if user sends valid data and receive otp code
        """
        data = {"phone_number":"09441234567","email":"test@email.com","password":"test","confirm_password":"test"}
        response = self.client.post(reverse("accounts:user_register"),data=data)    
        self.assertEqual(list(response.wsgi_request.session["user_data"].keys())[0],"09441234567")
        self.assertEqual(response.wsgi_request.session["user_data"]["09441234567"].get("email"),"test@email.com")
        self.assertEqual(OtpCode.objects.count(),1)
        self.assertEqual(response.data,{"Message":"We sent you a code , please check your email"})
        self.assertEqual(response.status_code,200)

    def test_invalid_data(self):
        """
        tests when user sends invalid data 
        """
        data = {"phone_number":"09441234567","email":"invalid_email","password":"test","confirm_password":"test"}
        response = self.client.post(reverse("accounts:user_register"),data=data)    
        self.assertEqual(response.data['email'][0],"Enter a valid email address.")
        self.assertEqual(response.status_code,400)


class TestUserVerifyCodeAPIView(APITestCase):

    def setUp(self):
        self.url = "accounts:user_verify_code"
        session = self.client.session
        session["user_data"] = {
            "09441234567":{
                "email":"test@email.com" , 
                "password":"test"
            }
        }
        session.save()
        self.otp_code = OtpCode.objects.create(email="test@email.com",code=1234)

    def test_send_valid_data_no_otp(self):
        """
        test when user sends valid data but no otp code would be found for the users' email
        """
        client = APIClient()
        session = client.session
        session["user_data"] = {
            "09441234567":{
                "email":"test1@email.com" , 
                "password":"test"
            }
        }
        session.save()
        otp_code1 = OtpCode.objects.create(email="test@email.com",code=1234)
        response = client.post(reverse(self.url),data={"code":1234})
        self.assertEqual(response.data , {"message":"No otp code for this email found"})
        self.assertEqual(response.status_code , 500)


    def test_send_valid_data_expired_otp(self):
        """
        test when user sends valid data but the otp code for the respective email is expired
        """
        self.otp_code.created = now() - timedelta(minutes=5)
        self.otp_code.save()
        response = self.client.post(reverse(self.url),data={"code":1234})
        self.assertTrue(self.otp_code.is_expired())
        self.assertEqual(response.data , {"message":"code is expired"})
        self.assertEqual(response.status_code , 500)

    
    def test_send_valid_data_wrong_code(self):
        """
        test if user sends valid data but the otp code is wrong and unmachted
        """
        response = self.client.post(reverse(self.url),data={"code":4321})
        self.assertEqual(response.data , {"mesaage":"Code is wrong,please try again"})
        self.assertEqual(response.status_code , 400)

    def test_send_valid_data(self):
        """
        test when user sends valid data and registered successfully
        """
        response = self.client.post(reverse(self.url),data={"code":1234})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(OtpCode.objects.count() ,0)
        self.assertIsNone(response.wsgi_request.session.get("user_data"))
        self.assertEqual(response.data, {"phone_number":"09441234567","email":"test@email.com"})
        self.assertEqual(response.status_code, 201)