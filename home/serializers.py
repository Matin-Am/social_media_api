from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields= ("user","body","description","file")
        extra_kwargs = {
            "body":{"required":True},
            "file":{"required":True},
            "description":{"required":True}
        }

    def get_user(self,obj):
        return f"{obj.user.phone_number} - {obj.user.email}"
        
    def create(self, validated_data ):
       request = self.context["request"]
       post = Post.objects.create(
           user = request.user , 
           body = validated_data.get("body"),
           description = validated_data.get("description") ,
           file = validated_data.get("file")
       )
       return post
    
    def update(self, instance, validated_data):
            instance.body = validated_data.get("body",instance.body)
            instance.description = validated_data.get("description",instance.description)
            instance.file = validated_data.get("file",instance.file)
            instance.save()
            return instance