from . import views
from django.urls import path


app_name = "accounts"
urlpatterns  = [
    path("register/",views.UserRegistrationAPIView.as_view(),name="user_register"),
    path("verify/",views.UserVerifyCodeAPIView.as_view(),name="user_verify_code"),
    path("login/",views.UserLoginAPIView.as_view(),name="user_login"),
    path("logout/",views.UserLogoutAPIView.as_view(),name="user_logout"),
    path("change_password/",views.ChangePasswordAPIView.as_view(),name="user_change_password")

]
