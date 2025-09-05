from rest_framework.permissions import BasePermission,SAFE_METHODS



class AdminOrIsowneronlyPermission(BasePermission):
    message = "Permission denied . You are not owner of this post !"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user 
    

class FollowOthersPermission(BasePermission):
    message = "You cant follow or unfollow yourself !"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user
    
    def has_object_permission(self, request, view, obj):
        return obj != request.user 