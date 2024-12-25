from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.views import APIView


from .models import *



class UserSerializer(serializers.ModelSerializer):
    extra_kwargs = {'password': {'write_only': True}}  # Không có cho xem password
    class Meta:
        model = User
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

    # Cái này xài bên giao diện admin của django nó không băm :))) để mò thêm
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data) #Update trừ pass


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'avatar', 'cover_avatar', 'role', 'phone_number', 'date_of_birth', 'gender', 'user']
class AlumniAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = AlumniAccount
        fields = ['account_id', 'alumni_account_code', 'account', 'confirm_status']

