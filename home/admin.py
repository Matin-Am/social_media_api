from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user","description","created")
    search_fields = ("description",)
    raw_id_fields = ("user",)
    list_filter = ("created",)