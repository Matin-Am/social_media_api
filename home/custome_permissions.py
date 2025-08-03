from rest_framework import permissions



class AdminOrIsowneronlyPermission(permissions.BasePermission):
    message = "Permission denied . You are not owner of this post !"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user 
    

class FollowOthersPermission(permissions.BasePermission):
    message = "You cant follow yourself !"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user
    
    def has_object_permission(self, request, view, obj):
        return obj != request.user 