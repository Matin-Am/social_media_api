from django.shortcuts import render , get_object_or_404 
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer,CommentSerializer
from .custome_permissions import AdminOrIsowneronlyPermission,FollowOthersPermission
from .models import Post,Relation,Comment
from accounts.models import User

# Create your views here.

# class PostViewSet(viewsets.ViewSet):
#     """
#     This Viewset is used for CRUD operations for our 'Post' model
#     CRUD operations:
#         C : creating post 
#         R : retrieve or reading post(s)
#         U : updating post
#         D : deleting post
#     """
#     authentication_classes = [TokenAuthentication]
#     permission_classes = []
#     serializer_class = PostSerializer


#     def get_queryset(self):
#         return Post.objects.all()
    

#     def list(self,request):
#         ser_data = self.serializer_class(self.get_queryset(),many=True)
#         return Response(ser_data.data,status=status.HTTP_200_OK)
    
#     def retrieve(self,request,pk=None):
#         post = get_object_or_404(self.get_queryset(),pk=pk)
#         ser_data = self.serializer_class(post).data
#         return Response(ser_data,status=status.HTTP_200_OK)


#     def partial_update(self,request,pk=None):
#         post = get_object_or_404(self.get_queryset(),id=pk)
#         self.check_object_permissions(request,post)
#         ser_data = self.serializer_class(data=request.data,instance=post,partial=True)
#         if ser_data.is_valid():
#             new_post = ser_data.save()
#             return Response(self.serializer_class(new_post).data,status=status.HTTP_200_OK)
#         return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    

#     def create(self,request):
#         ser_data = self.serializer_class(data=request.data,context={"request":request})
#         if ser_data.is_valid():
#             post = ser_data.save()
#             return Response(self.serializer_class(post).data,status=status.HTTP_200_OK)
#         return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def destroy(self,request,pk=None):
#         post = get_object_or_404(self.get_queryset(),pk=pk)
#         self.check_object_permissions(request,post)
#         post.delete()
#         return Response({"Message":"Post deleted sucessfully"},status=status.HTTP_200_OK)

#     def get_permissions(self):
#         if self.action == "destroy" or self.action == "partial_update":
#             self.permission_classes = [AdminOrIsowneronlyPermission]
#         if self.action == "create":
#             self.permission_classes = [IsAuthenticated]
#         return [permission() for permission in self.permission_classes]
    
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = []
    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()

    def partial_update(self, request, *args, **kwargs):
        self.check_object_permissions(request,self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_object_permissions(request,self.get_object())
        return super().destroy(request, *args, **kwargs)
    
    def get_permissions(self):
        if self.action == "destroy" or self.action == "partial_update":
            self.permission_classes = [AdminOrIsowneronlyPermission]
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]




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
    authentication_classes = [TokenAuthentication]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = User.objects.annotate(
            followers_count=Count("followers",distinct=True),
            followings_count=Count("followings",distinct=True)
        ).values("id","email","followers_count","followings_count")
        return Response({"users":users})

class CreateCommentAPI(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self,request,post_id,comment_id=None):
        reply_to=None
        post = get_object_or_404(Post,pk=post_id)
        if comment_id:
            reply_to = get_object_or_404(Comment,pk=comment_id)
        ser_data = self.serializer_class(data=request.data,context={
            "request":request,
            "post":post,
            "reply_to":reply_to
        })
        if ser_data.is_valid(raise_exception=True):
            comment=ser_data.save()
            return Response(self.serializer_class(comment).data,status=status.HTTP_200_OK)
