from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
def validate_file_extentions(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Post(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=400)
    description = models.TextField(max_length=100)
    file = models.FileField(upload_to="uploads/",validators=[validate_file_extentions,])
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.description}"