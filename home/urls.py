from . import views
from django.urls import path
from rest_framework import routers

app_name = "home"
urlpatterns  = [
    path("follow/<int:user_id>/",views.UserFollowAPI.as_view()),
    path("unfollow/<int:user_id>/",views.UserUnfollowAPI.as_view()),
    path("relations/",views.AllUsersListRelationAPI.as_view()),
    path("relations/<int:user_id>/",views.UserListRelationsAPI.as_view())
]

router = routers.SimpleRouter()
router.register("post",views.PostViewSet,basename="post")
urlpatterns += router.urls