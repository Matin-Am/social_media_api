from . import views
from django.urls import path


app_name = "accounts"
urlpatterns  = [
    path("register/",views.UserRegistrationAPI.as_view()),
    path("verify/",views.UserVerifyCodeAPI.as_view()),
    path("logout/",views.UserLogoutAPI.as_view())

]
