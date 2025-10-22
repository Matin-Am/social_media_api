from datetime import timedelta
from rest_framework.test import APITestCase,APIClient,APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from django.urls import reverse
from django.utils.timezone import now
from unittest.mock import patch
from ..models import OtpCode,User
from ..views import UserLogoutAPIView,ChangePasswordAPIView

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

class TestUserRegistrationAndUserVerifyCodeFlow(APITestCase):

    def test_register_and_verify(self):
        """
        test the flow of the registraion and verifying code 
        """
        data = {"phone_number":"09441234567","email":"test@email.com","password":"test","confirm_password":"test"}
        response = self.client.post(reverse("accounts:user_register"),data=data)
        self.assertIsNotNone(response.wsgi_request.session["user_data"])
        self.assertEqual(response.data,{"Message":"We sent you a code , please check your email"})
        otp_code = OtpCode.objects.first()
        response2 = self.client.post(reverse("accounts:user_verify_code"),data={"code":otp_code.code})
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response2.status_code,201)



class TestUserLogoutAPIView(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(phone_number="09441234567",email="test@email.com",password="test")
        self.url = "accounts:user_logout"

    def test_logging_authenticated_user_out(self):
        """
        test when an authenticated user calls this api , his Token will be deleted and logged out from system 
        """
        request = self.factory.post(reverse(self.url))
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = UserLogoutAPIView.as_view()(request)
        self.assertEqual(Token.objects.count(),0)
        self.assertEqual(response.data,{"message":"Logged out successfully"})
        self.assertEqual(response.status_code,204)


    def test_logging_unauthenticated_user_out(self):
        """
        test when an unauthenticated user calls this api , he will come up with 401 error
        """
        request = self.factory.post(reverse(self.url))
        response = UserLogoutAPIView.as_view()(request)
        self.assertEqual(Token.objects.count(),1)
        self.assertEqual(response.data["detail"],"Authentication credentials were not provided.")
        self.assertEqual(response.status_code,401)


class TestChangePasswordAPIView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number="09441234567",email="test@email.com",password="test")
        self.factory = APIRequestFactory()
        self.url = "accounts:user_change_password"


    def test_wrong_password(self):
        """
        test if user sends his old password wrong
        """
        data = {"old_password":"wrong_pass","new_password":"new_test"}
        request = self.factory.post(reverse(self.url),data=data)
        force_authenticate(request,user=self.user,token=self.user.auth_token)
        response = ChangePasswordAPIView.as_view()(request)
        self.assertEqual(response.data,{"Old password":"Wrong password !"})
        self.assertEqual(response.status_code,400)
    

    def test_correct_password(self):
        """
        test if user sends his old password correct and new password will be saved in database
        """
        data = {"old_password":"test","new_password":"new_test"}
        request = self.factory.post(reverse(self.url),data=data)
        force_authenticate(request,user=self.user,token=self.user.auth_token)
        response = ChangePasswordAPIView.as_view()(request)
        self.assertEqual(response.data,{"Message":"Password changed successfully"})
        self.assertEqual(response.status_code,200)
        