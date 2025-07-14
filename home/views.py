from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import PostSerializer
from .custome_permissions import AdminOrIsowneronlyPermission
from .models import Post
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
    serializer_class = PostSerializer
    def put(self,request,post_id):
        post = Post.objects.get(pk=post_id)
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