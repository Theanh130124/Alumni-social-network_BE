from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'avatar', 'cover_avatar', 'role', 'phone_number', 'date_of_birth', 'gender', 'user']
class AlumniAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = AlumniAccount
        fields = ['account_id', 'alumni_account_code', 'account', 'confirm_status']

# class RoleSerializer(serializers.Serializer):
#     value = serializers.CharField()
#     name = serializers.CharField()
#
#
#
# class SurveyQuestionTypeSerializer(ModelSerializer):
#     class Meta:
#         model = SurveyQuestion
#         fields = '__all__'
#
# #InvationGroup
# class AccountSerializerForInvitationGroup(ModelSerializer):
#     avatar = serializers.SerializerMethodField(source='avatar')
#     cover_avatar = serializers.SerializerMethodField(source='cover_avatar')
#     @staticmethod
#     def get_avatar(account):
#         if account.avatar:
#             return account.avatar.name
#     @staticmethod
#     def get_cover_avatar(account):
#         if account.cover_avatar:
#             return account.cover_avatar.name
#
#     class Meta:
#         model = Account
#         fields = '__all__'
#
# #InvationGroup ####
# class CrateInvitationGroupSerializer(ModelSerializer):
#     id = serializers.IntegerField(source='pk',read_only=True)
#     class Meta:
#         model = InvitationGroup
#         fields = ['id','invitation_group_name']
#
#
# class UpdateInvitationGroupSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='pk', read_only=True)
#
#     class Meta:
#         model = InvitationGroup
#         fields = ['id', 'invitation_group_name']
#
#
# class InvitationGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvitationGroup
#         fields = '__all__'
#
# class UserSerializerForInvitationGroup(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']
#
# ###
# class UserSerializerForSearch(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username','first_name' , 'last_name' ,"email"]
#
#
# # Đã fix
# class AccountSerializerForUser(serializers.ModelSerializer):
#     user = UserSerializerForSearch()
#     role = serializers.SerializerMethodField()  # Sử dụng SerializerMethodField để chuyển đổi Enum Role
#
#     avatar = serializers.SerializerMethodField()
#     cover_avatar = serializers.SerializerMethodField()
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         # Tùy chỉnh hiển thị role nếu cần thêm
#         representation['role'] = representation['role']  # `role` đã xử lý qua `get_role`
#         return representation
#
#     @staticmethod
#     def get_role(account):
#         """Chuyển giá trị Enum Role sang định dạng JSON."""
#         if account.role:  # Giả định account.role lưu giá trị value của Role Enum
#             for role in Role:
#                 if role.value == account.role:
#                     return {"value": role.value, "name": role.name}
#         return None
#
#     @staticmethod
#     def get_avatar(account):
#         """Xử lý avatar."""
#         if account.avatar:
#             return account.avatar.url if hasattr(account.avatar, 'url') else account.avatar.name
#
#     @staticmethod
#     def get_cover_avatar(account):
#         """Xử lý cover avatar."""
#         if account.cover_avatar:
#             return account.cover_avatar.url if hasattr(account.cover_avatar, 'url') else account.cover_avatar.name
#
#     class Meta:
#         model = Account
#         fields = ['user', 'avatar', 'cover_avatar', 'phone_number', 'role']