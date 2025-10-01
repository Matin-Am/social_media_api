import time
from django.shortcuts import get_object_or_404 
from django.db.models import Count
from django.core.cache import cache
from django.utils.http import urlencode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import generics
from .serializers import PostSerializer,CommentSerializer
from .custome_permissions import AdminOrIsowneronlyPermission,FollowOthersPermission
from .models import Post,Relation,Comment
from .paginations import DefaultPagination
from .filters import PostFilter
from accounts.models import User

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    """
    This ModelViewset is used for CRUD operations for our 'Post' model
    CRUD operations:
        C : creating post 
        R : retrieve or reading post(s)
        U : updating post
        D : deleting post
     """
    serializer_class = PostSerializer
    permission_classes = []
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = PostFilter
    search_fields = ["body","description"]
    queryset = Post.objects.all()
    
    def get_permissions(self):
        if self.action in ("update","partial_update","destroy"):
            self.permission_classes = [AdminOrIsowneronlyPermission]
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        params = urlencode(sorted(request.GET.items()))
        cached_key = f"list_posts_{request.user.id}_{params}" or f"list_posts_anon"
        cached_data = cache.get(cached_key)
        if cached_data is None:
            result = super().list(request, *args, **kwargs)
            cache.set(cached_key,result.data,timeout= 60 * 15)
            return result
        return Response(cached_data)
    
class UserFollowAPI(APIView):
    """
        With this api user is able to unfollow other users
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [FollowOthersPermission]
    def post(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        self.check_object_permissions(request,user)
        relation , created = Relation.objects.get_or_create(from_user=request.user,to_user=user)
        if created is False:
            return Response({"message":"You already followed this user"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You followed this user"},status=status.HTTP_200_OK)
    
class UserUnfollowAPI(APIView):
    """
    With this api user is able to unfollow other users
    """
    permission_classes = [FollowOthersPermission]
    authentication_classes = [TokenAuthentication]
    def delete(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        self.check_object_permissions(request,user)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            relation.delete()
            return Response({"Message":"User unfollowed successfully"},status=status.HTTP_200_OK)
        return Response({"Error":"You are already not following this user"},status=status.HTTP_400_BAD_REQUEST)
    
class UserListRelationsAPI(APIView):
    """
    This api shows all relations of a specific user 
    """
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
       user = get_object_or_404(User,pk=user_id)
       followers = user.followers.count()
       followings = user.followings.count()
       return Response({
            "user": {
                "id": str(user.id),
                "email": str(user.email),
                "followers": followers ,
                "followings": followings
            }
        },status=status.HTTP_200_OK)
    
class AllUsersListRelationAPI(APIView):
    """
    This api shows the whole relations(followers and followings) of all users 
    """
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = User.objects.annotate(
            followers_count=Count("followers",distinct=True),
            followings_count=Count("followings",distinct=True)
        ).values("id","email","followers_count","followings_count")
        paginator = PageNumberPagination()
        paginator.page_size = 2
        results = paginator.paginate_queryset(users,request)
        return paginator.get_paginated_response(results)


class PostCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post","user"]

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        post_id = self.kwargs.get("post_id")
        if comment_id is not None: 
            return Comment.objects.filter(post__id=post_id,reply_to__id=comment_id,is_reply=True)
        return Comment.objects.filter(post__id=post_id)
    
    def get_serializer_context(self):
        reply_to=None
        post = get_object_or_404(Post,pk=self.kwargs.get("post_id"))
        if self.kwargs.get("comment_id"):
            reply_to = get_object_or_404(Comment,pk=self.kwargs["comment_id"])
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            "post":post ,
            "reply_to":reply_to
        }
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]