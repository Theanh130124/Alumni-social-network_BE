from django.core.serializers import serialize
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from urllib3 import request
from django.utils import timezone
#Serializer validate + json -> python object

from .models import *
from .permissions import CommentOwner





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
            instance.password_changed_at = timezone.now() #Nếu người dùng đổi pass thì set lại time
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

    #Comment-----------
class CommentForCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_content', 'comment_image_url', 'account', 'post']

class CommentForUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_content', 'comment_image_url',]


class CommentSerializer(serializers.ModelSerializer):
    comment_image_url = serializers.SerializerMethodField(source='comment_image_url')


    class Meta:
        model = Comment
        fields = '__all__'

#------------
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'



class AccountForPostReaction(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'avatar', 'cover_avatar']
class PostForPostReaction(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["post_content"]
#Có thể lấy ảnh ra -> lấy được bình luận đó vừa bình luận vào bài viết nào
class PostReactionSerializer(serializers.ModelSerializer):
        #Viết như thế -> thì khi trả ve account -> nó trả chi tiet chu khong tra account_id :
        account = AccountForPostReaction()
        post = PostForPostReaction()
        class Meta:
            model = PostReaction
            fields = '__all__'

class PostReactionForCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ['id','reaction','post','account']

class PostReactionForUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ['id','reaction','post']

#PostInvitation ---

class PostInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostInvitation
        fields = '__all__'
class PostInvitationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostInvitation
        fields = ['id', 'event_name', 'start_time', 'end_time', 'post']


class PostInvitationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostInvitation
        fields = ['id', 'event_name', 'start_time', 'end_time']

class AlumniForInvitationSerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = AlumniAccount
        fields = '__all__'

###--------

##PostSurvey

class PostSurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = PostSurvey
        fields = '__all__'


class PostSurveyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = PostSurvey
        fields = ['id', 'post_survey_title', 'start_time', 'end_time', 'post']

#Xử lý cái is_closed
class PostSurveyUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = PostSurvey
        fields = ['id', 'post_survey_title', 'start_time', 'end_time', 'is_closed']