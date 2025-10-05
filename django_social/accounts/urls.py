from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView,TokenBlacklistView

app_name = "accounts"
urlpatterns  = [
    # Registration 
    path("register/",views.UserRegistrationAPIView.as_view(),name="user_register"),
    path("verify/",views.UserVerifyCodeAPIView.as_view(),name="user_verify_code"),
    # Token Authentication 
    path("login/",views.UserLoginAPIView.as_view(),name="user_login"),
    path("logout/",views.UserLogoutAPIView.as_view(),name="user_logout"),
    # JWT Authentication 
    path("jwt/create/",views.JwtTokenObtainPairView.as_view(),name="jwt-create"),
    path("jwt/refresh/",TokenRefreshView.as_view(),name="jwt-refresh"),
    path("jwt/verify/",TokenVerifyView.as_view(),name="jwt-verify"),
    path("jwt/logout/",views.JwtTokenLogoutAPIView.as_view(),name="jwt-logout"),
    # Change password
    path("change_password/",views.ChangePasswordAPIView.as_view(),name="user_change_password")

]
