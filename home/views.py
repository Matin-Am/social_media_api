from django.shortcuts import render , get_object_or_404 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import PostSerializer
from .custome_permissions import AdminOrIsowneronlyPermission , FollowOthersPermission
from rest_framework.permissions import IsAuthenticated
from .models import Post , Relation
from accounts.models import User
from rest_framework.viewsets import ViewSet
# Create your views here.

class UserListPostsAPI(APIView):
    serializer_class = PostSerializer
    def get(self,request):
       posts = Post.objects.all()
       ser_data = self.serializer_class(instance=posts,many=True)
       return Response(ser_data.data)


class UserCreatePostAPI(APIView):
    authentication_classes = [TokenAuthentication,]
    serializer_class = PostSerializer
    def post(self,request):
        ser_data = self.serializer_class(data=request.data,context={"request":request})
        if ser_data.is_valid():
            post = ser_data.create(ser_data.validated_data)
            return Response(data=self.serializer_class(post).data,status=status.HTTP_201_CREATED)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserUpdatePostAPI(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [AdminOrIsowneronlyPermission]
    serializer_class = PostSerializer
    def put(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        self.check_object_permissions(request,post)
        ser_data =  self.serializer_class(data=request.data, instance=post,partial=True)
        if ser_data.is_valid():
            post = ser_data.save()  
            return Response(self.serializer_class(post).data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserDeletePostAPI(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [AdminOrIsowneronlyPermission,]
    def delete(self,request,post_id):
        post = get_object_or_404(Post , id = post_id)
        self.check_object_permissions(request , post)
        post.delete()
        return Response({"message":"post has been deleted successfully"},status=status.HTTP_200_OK)
    
class UserFollowAPI(APIView):
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
    def delete(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            relation.delete()
            return Response({"Message":"User unfollowed successfully"},status=status.HTTP_200_OK)
        return Response({"Error":"You are already not following this user"},status=status.HTTP_400_BAD_REQUEST)
    
class UserListRelationAPI(APIView):
    def get(self,request):
        pass