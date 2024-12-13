from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import default


class BaseEnum(Enum):
    @classmethod
    def choices(cls): #-> cls là UserRole
        return [(key.value, key.name) for key in cls] #[ ADMIN : "Quản trị viên"  , " " ...  ]

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    deleted_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ordering = ['-id'] # Bản ghi mới tạo sẽ hiện trước


class Role(BaseEnum):
    ADMIN = "Quản trị viên"
    LECTURER = "Giảng viên"



class ConfirmStatus(BaseEnum):
    PENDING = "Chờ xác nhận"
    CONFIRMED = "Đã xác nhận"
    REJECTED = "Đã từ chối"


class User(AbstractUser):
    confirm_status = models.CharField(
        max_length=50,
        choices=ConfirmStatus.choices(),
        default=ConfirmStatus.PENDING.name
    )

    def __str__(self):
        return self.username

class Account(BaseModel):
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    avatar = CloudinaryField('avatar' , default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1732632586/pfvvxablnkaeqmmbqeit.png" , blank='True')
    cover_avatar = CloudinaryField('cover' ,default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1733331571/hvyl33kneih3lsn1p9hp.png" ,blank= 'True')
    account_status = models.BooleanField(default=False)
    gender = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True) #Có primary_key django tạo thay id thành acount_id
    role = models.CharField(
        max_length=50,
        choices=Role.choices(),
        default=Role.LECTURER.value
    )
    def __str__(self):
        return self.user.username

#TK Cựu SV
class AlumniAccount(BaseModel):
    alumni_account_code = models.CharField(max_length=50 ,unique=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE ,primary_key=True)

    def __str__(self):
        return self.alumni_account_code
class Post(BaseModel):
    post_content = RichTextField()
    comment_lock = models.BooleanField(default=False)
    account = models.ForeignKey(Account,  on_delete=models.CASCADE, null=True , related_name="posts")

    def __str__(self):
        return self.post_content
#Like , Haha , Tym
class Reaction(BaseEnum):
    LIKE = "Like"
    HAHA = "Haha"
    TYM = " Thả tym"

#Chi tiết reaction
class PostReaction(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True ,related_name='post_reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='post_reactions')
    reaction = models.CharField(max_length=50,
                                choices=Reaction.choices(),
                                default=None)

#Hình của post
class PostImage(BaseModel):
    post_image_url = CloudinaryField(blank=True , null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='post_images')

    def __str__(self):
        return self.post_image_url.name


class Comment(BaseModel):
    comment_content = models.TextField()
    comment_image_url = CloudinaryField(blank = True , null=True )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True , related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE ,  related_name='comments')

    def __str__(self):
        return self.comment_content

#Post Khảo sát
class PostSurvey(BaseModel):
    post_survey_title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.post_survey_title

#Xem xét Enum
class SurveyQuestionType(BaseModel):
    question_type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.question_type_name

#Câu hỏi
class SurveyQuestion(BaseModel):
    question_content = models.TextField()
    question_order = models.IntegerField()
    is_required = models.BooleanField(default=False)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE ,related_name='survey_questions')
    survey_question_type = models.ForeignKey(SurveyQuestionType, on_delete=models.CASCADE ,related_name='survey_questions')

    def __str__(self):
        return self.question_content
#Lựa chọn
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

#
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