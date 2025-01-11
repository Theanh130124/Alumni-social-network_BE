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
        if view.action in ['update', 'partial_update',]:
            return request.user == post.account.user #Đã bỏ quyền admin xóa bài
        if view.action == 'destroy':
            return request.user == post.account.user \
                or request.user.account.role == UserRole.ADMIN #admin cũng được xóa post
        return False
#Người thả mới được update và xóa
class PostReactionOwner(BasePermission):
    def has_object_permission(self, request, view, post_reaction):
        return request.user.account == post_reaction.account
#Chủ post , người comment hoặc admin sẽ xóa được
class CommentOwner(BasePermission):
    def has_object_permission(self, request, view, comment):
        if view.action == 'destroy':
            return request.user == comment.post.account.user \
                or request.user == comment.account.user  #Đã bỏ quyền admin xóa comment
        elif view.action in ['update', 'partial_update']:
            return request.user == comment.account.user