from rest_framework import permissions



class AdminOrIsowneronlyPermission(permissions.BasePermission):
    message = "Permission denied . You are not owner of this post !"
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.user 