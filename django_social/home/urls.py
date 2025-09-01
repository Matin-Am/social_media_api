from . import views
from django.urls import path
from rest_framework import routers

app_name = "home"
urlpatterns  = [
    path("follow/<int:user_id>/",views.UserFollowAPI.as_view(),name="user_follow"),
    path("unfollow/<int:user_id>/",views.UserUnfollowAPI.as_view(),name="user_unfollow"),
    path("relations/",views.AllUsersListRelationAPI.as_view(),name="relations"),
    path("relations/<int:user_id>/",views.UserListRelationsAPI.as_view(),name="user_relations"),
    path("comment/<int:post_id>/",views.CreateCommentAPI.as_view(),name="create_comment"),
    path("comment/<int:post_id>/<int:comment_id>/",views.CreateCommentAPI.as_view(),name="reply_comment")
]

router = routers.DefaultRouter()
router.register("post",views.PostViewSet,basename="post")
urlpatterns += router.urls