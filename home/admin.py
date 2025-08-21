from django.contrib import admin
from .models import Post , Relation,Comment
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user","description","created")
    search_fields = ("description",)
    raw_id_fields = ("user",)
    list_filter = ("created",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user","post","is_reply","reply_to")
    list_filter = ("is_reply","user")
    search_fields = ("body",)
    ordering = ("-created",)
    raw_id_fields = ("user",)

admin.site.register(Relation)
