from . import views
from django.urls import path

app_name = "home"
urlpatterns  = [
    path("create/",views.UserCreatePostAPI.as_view()),
    path("update/<int:post_id>/",views.UserUpdatePostAPI.as_view()),
    path("list/",views.UserListPostsAPI.as_view()), 
    path("delete/<int:post_id>/",views.UserDeletePostAPI.as_view())
]