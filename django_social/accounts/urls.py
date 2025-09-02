from . import views
from django.urls import path
from rest_framework.authtoken import views as token_views 

app_name = "accounts"
urlpatterns  = [
    path("register/",views.UserRegistrationAPIView.as_view(),name="user_register"),
    path("verify/",views.UserVerifyCodeAPIView.as_view(),name="user_verify_code"),
    path("login/",token_views.obtain_auth_token,name="user_login"),
    path("logout/",views.UserLogoutAPIView.as_view(),name="user_logout"),
    path("change_password/",views.ChangePasswordAPIView.as_view(),name="user_change_password")

]
