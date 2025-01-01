from rest_framework.permissions import BasePermission
from Sociales.models  import *
from rest_framework import  permissions
from Sociales.models  import *

class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account.role == UserRole.ADMIN

#Quyền bài viết


class PostOwner(BasePermission):
    def has_object_permission(self, request, view, post):  # Truyền post vào
        if view.action == 'destroy':
            return request.user == post.account.user or request.user.account.role == UserRole.ADMIN
        if view.action in ['update', 'partial_update']:
            return request.user == post.account.user
        return False

