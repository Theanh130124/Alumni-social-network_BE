from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import default

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    deleted_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id'] # Bản ghi mới tạo sẽ hiện trước


class Role(Enum):
    ADMIN = "Quản trị viên"
    LECTURER = "Giảng viên"

    @classmethod
    def choices(cls): #-> cls là UserRole
        return [(key.value, key.name) for key in cls]  #[ ADMIN : "Quản trị viên"  , " " ...  ]

#Trang thái
class ConfirmStatus(BaseModel):
    confirm_status_value = models.CharField(max_length=50)

    def __str__(self):
        return self.confirm_status_value


class User(AbstractUser):
    confirm_status = models.ForeignKey(ConfirmStatus, on_delete=models.CASCADE) #, default=3)

    def __str__(self):
        return self.username


class Account(BaseModel):
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    avatar = CloudinaryField('avatar' , default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1732632586/pfvvxablnkaeqmmbqeit.png" , blank='True')
    cover_avatar = CloudinaryField('cover' ,default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1733331571/hvyl33kneih3lsn1p9hp.png" ,blank= 'True')
    account_status = models.BooleanField(default=False)
    gender = models.BooleanField(default=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True ,primary_key=True) #Có primary_key django tạo thay id
    role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.LECTURER.value
    )
    def __str__(self):
        return self.user.username

#TK Cựu SV
class AlumniAccount(BaseModel):
    alumni_account_code = models.CharField(max_length=50)
    account = models.OneToOneField(Account, on_delete=models.CASCADE ,primary_key=True)

    def __str__(self):
        return self.alumni_account_code
#Bài Viết
class Post(BaseModel):
    post_content = RichTextField()
    comment_lock = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.post_content

#Like , Haha , Tym
class Reaction(BaseModel):
    reaction_name = models.CharField(max_length=255)

    def __str__(self):
        return self.reaction_name

#M2M post vs reaction
class PostReaction(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)


class PostImage(BaseModel):
    post_image_url = CloudinaryField(blank=True , null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_image_url.name


class Comment(BaseModel):
    comment_content = models.TextField()
    comment_image_url = CloudinaryField(blank = True , null=True )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content


class PostSurvey(BaseModel):
    post_survey_title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_survey_title


class SurveyQuestionType(BaseModel):
    question_type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.question_type_name


class SurveyQuestion(BaseModel):
    question_content = models.TextField()
    question_order = models.IntegerField()
    is_required = models.BooleanField(default=False)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE)
    survey_question_type = models.ForeignKey(SurveyQuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_content

class SurveyQuestionOption(BaseModel):
    question_option_value = models.TextField()
    question_option_order = models.IntegerField()
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    survey_answers = models.ManyToManyField('SurveyAnswer', blank=True)

    def __str__(self):
        return self.question_option_value


class SurveyResponse(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + ' - ' + self.post_survey.post_survey_title


class SurveyAnswer(BaseModel):
    answer_value = models.CharField(max_length=10000, null=True, blank=True)
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)

    def __str__(self):
        if not self.answer_value:
            return 'Not input text type' + \
                   ' (' + self.survey_question.question_content + ' - ' + self.survey_response.__str__() + ') '
        else:
            return self.answer_value


# class SurveyAnswerOption(BaseModel):
#     survey_question_option = models.ForeignKey(SurveyQuestionOption, on_delete=models.CASCADE)
#     survey_answer = models.ForeignKey(SurveyAnswer, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.survey_answer.__str__() + self.survey_question_option.__str__()


class PostInvitation(BaseModel):
    event_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    accounts = models.ManyToManyField('Account', blank=True)

    def __str__(self):
        return self.event_name


class InvitationGroup(BaseModel):
    invitation_group_name = models.CharField(max_length=255)
    accounts = models.ManyToManyField('Account', blank=True)

    def __str__(self):
        return self.invitation_group_name


# class GroupAccount(BaseModel):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     invitation_group = models.ForeignKey(InvitationGroup, on_delete=models.CASCADE)


# class InvitationAccount(BaseModel):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     post_invitation = models.ForeignKey(PostInvitation, on_delete=models.CASCADE)

class Room(BaseModel):
    # roomId = 1
    # khang -> theanh ||| roomName = 1
    # theanh -> khang ||| roomName = 1
    # id sender + id receiver => room Id
    first_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='first_user_room', null=True)
    second_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='second_user_room', null=True)
    received_message_date = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ['first_user', 'second_user']

    def __str__(self):
        return str(self.first_user.id) + str(self.second_user.id)


class Message(BaseModel):
    who_sent = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=10000)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content