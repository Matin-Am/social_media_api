from . import views
from django.urls import path
from rest_framework.authtoken import views as token_views 

app_name = "accounts"
urlpatterns  = [
    path("register/",views.UserRegistrationAPI.as_view()),
    path("verify/",views.UserVerifyCodeAPI.as_view()),
    path("login/",token_views.obtain_auth_token),
    path("logout/",views.UserLogoutAPI.as_view())

]
