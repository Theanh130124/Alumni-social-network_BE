from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer

from .models import *

#Dùng cho dropdown
class EnumCollectionSerializer(serializers.Serializer):
    reaction = serializers.SerializerMethodField()
    survey_question_type = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    confirm_status =serializers.SerializerMethodField()
    def get_reaction(self,obj):
        return [{"key":item.name,"value": item.value} for item in Reaction]
    def get_survey_question_type(self ,obj):
        return [{"key": item.name, "value": item.value} for item in SurveyQuestionType]
    def get_role(self,obj):
        return [{"key": item.name, "value": item.value} for item in Role]
    def get_confirm_status(self,obj):
        return [{"key": item.name, "value": item.value} for item in ConfirmStatus]


class SurveyQuestionTypeSerializer(ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'

#InvationGroup
class AccountSerializerForInvitationGroup(ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')
    cover_avatar = serializers.SerializerMethodField(source='cover_avatar')
    @staticmethod
    def get_avatar(account):
        if account.avatar:
            return account.avatar.name
    @staticmethod
    def get_cover_avatar(account):
        if account.cover_avatar:
            return account.cover_avatar.name

    class Meta:
        model = Account
        fields = '__all__'

#InvationGroup ####
class CrateInvitationGroupSerializer(ModelSerializer):
    id = serializers.IntegerField(source='pk',read_only=True)
    class Meta:
        model = InvitationGroup
        fields = ['id','invitation_group_name']


class UpdateInvitationGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = InvitationGroup
        fields = ['id', 'invitation_group_name']


class InvitationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationGroup
        fields = '__all__'

class UserSerializerForInvitationGroup(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

###
class UserSerializerForSearch(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name' , 'last_name' ,"email"]

class AccountSerializerForUser(serializers.ModelSerializer):
    user = UserSerializerForSearch()
    role = serializers.SerializerMethodField()

    avatar = serializers.SerializerMethodField(source='avatar')
    cover_avatar = serializers.SerializerMethodField(source='cover_avatar')

    def get_role(self, obj):
        return {"value": obj.role.value} #Xem xet

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = str(representation['role']['id']) + '/' + representation['role']['role_name']
        return representation

    @staticmethod
    def get_avatar(account):
        if account.avatar:
            return account.avatar.name

    @staticmethod
    def get_cover_avatar(account):
        if account.cover_avatar:
            return account.cover_avatar.name

    class Meta:
        model = Account
        fields = ['user', 'avatar', 'cover_avatar', 'phone_number', 'role']