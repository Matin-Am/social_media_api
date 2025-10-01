from rest_framework import serializers
from .models import Post  ,Comment
from django.utils.text import slugify
from rest_framework.reverse import reverse


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    relative_url = serializers.URLField(source="get_absolute_url",read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="abs_url",read_only=True)
    class Meta:
        model = Post
        fields= ("user","body","description","id","relative_url","absolute_url")
        extra_kwargs = {
            "body":{"required":True},
            "file":{"required":True},
            "description":{"required":True}
        }

    def get_user(self,obj):
        return f"{obj.user.phone_number} - {obj.user.email}"
    
    def abs_url(self,obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def to_representation(self, instance):
        request = self.context.get("request")
        rep =  super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url",None)
            rep.pop("absolute_url",None)
        return rep

    def create(self, validated_data ):
       request = self.context["request"]
       post = Post.objects.create(
           user = request.user , 
           body = validated_data.get("body"),
           slug = slugify(validated_data.get("body")[:30]),
           description = validated_data.get("description") ,
           file = validated_data.get("file")
       )
       return post
    
    def update(self, instance, validated_data):
            instance.body = validated_data.get("body",instance.body)
            instance.slug = validated_data.get("slug",slugify(instance.body)[:30])
            instance.description = validated_data.get("description",instance.description)
            instance.file = validated_data.get("file",instance.file)
            instance.save()
            return instance


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.SlugRelatedField(read_only=True,slug_field="slug")
    class Meta: 
        model = Comment
        fields = ("body","user","post","reply_to","is_reply")
        extra_kwargs = {
            "body":{"required":True},
            "reply_to":{"read_only":True},
            "is_reply":{"read_only":True},
        }

    def create(self, validated_data):
        is_reply=False
        request = self.context.get("request")
        post = self.context.get("post")
        reply_to = self.context.get("reply_to")
        if reply_to:
            if reply_to and reply_to.post != post:
                raise serializers.ValidationError('Reply comment must belong to the same post !')
            is_reply=True
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=validated_data.get("body"),
            reply_to=reply_to,
            is_reply=is_reply

        )
        return comment