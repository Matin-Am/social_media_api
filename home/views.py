from django.shortcuts import render , get_object_or_404 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import PostSerializer
from .custome_permissions import AdminOrIsowneronlyPermission 
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
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        if user == request.user:
            return Response({"message":"You can't follow yourself ! "},status=status.HTTP_400_BAD_REQUEST)
        relation = Relation.objects.get_or_create(from_user=request.user,to_user=user)
        if not relation:
            return Response({"message":"You already followed this user"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You followed this user"},status=status.HTTP_200_OK)
    
