from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import os
from django.core.exceptions import ValidationError

# Create your models here.
def validate_file_extentions(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Post(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(null=True,blank=True)
    body = models.TextField(max_length=400)
    description = models.TextField(max_length=100)
    file = models.FileField(upload_to="posts/",validators=[validate_file_extentions,])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user} - {self.description}"
    
    def get_absolute_url(self):
        return reverse("home:post-detail",kwargs={"pk":self.pk})

class Relation(models.Model):
    from_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE , related_name="followings",db_column="from_user")
    to_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="followers",db_column="to_user")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "relation"

    def __str__(self):
        return f"{self.from_user.phone_number} is following {self.to_user.phone_number}"



class Comment(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="ucomments")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    reply_to = models.ForeignKey("Comment",on_delete=models.SET_NULL,related_name="rcomments",null=True,blank=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user}: {self.body[:30]}"