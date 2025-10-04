from django.urls import reverse,resolve
from rest_framework.test import APISimpleTestCase
from ..views import (UserRegistrationAPIView,UserVerifyCodeAPIView,
                     UserLoginAPIView,UserLogoutAPIView,ChangePasswordAPIView)



info = {
    "user_register":UserRegistrationAPIView , 
    "user_verify_code":UserVerifyCodeAPIView , 
    "user_login":UserLoginAPIView , 
    "user_logout":UserLogoutAPIView , 
    "user_change_password":ChangePasswordAPIView
}
class TestAcoountsUrls(APISimpleTestCase):

        def test_urls(self):
            for name , view in info.items():
                url = reverse(f"accounts:{name}")
                self.assertEqual(resolve(url).func.view_class ,view)