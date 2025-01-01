from django.core.serializers import serialize
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from urllib3 import request

#Serializer validate + json -> python object

from .models import *

#Các trường update , create muốn validate kĩ thì def viết bên này bên view gọi action qua
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # lúc get list không xem pass

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email' ]
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'first_name', 'last_name', 'email' ]
        extra_kwargs = {'username': {'read_only':True} , 'password' :{'write_only':True}} #Khong cap nhat usernam khong thay pass moi cap nhat
    #Ten tk co update dc ??
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data) #gọi update của ModelSerializer -> update trừ pass

#Dành cho update
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'avatar', 'cover_avatar', 'role', 'phone_number', 'date_of_birth', 'gender', 'user' ]
        extra_kwargs = {'role': {'read_only': True}}



class AlumniAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = AlumniAccount
        fields = ['account_id', 'alumni_account_code', 'account', 'confirm_status']
        extra_kwargs = {'alumni_account_code': {'read_only': True}}

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id' , 'post_content' , 'created_date' , 'updated_date' , 'account' , 'comment_lock']
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['account'] = user.account
        return  super().create(validated_data)


