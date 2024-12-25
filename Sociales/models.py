from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import default
from django.db.models import TextChoices



class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ordering = ['-id'] # Bản ghi mới tạo sẽ hiện trước
class Gender(TextChoices):
    Nam = "Male","Nam"
    Nu = "Female","Nữ"

class UserRole(TextChoices):
    ADMIN = "Admin", "Quản trị viên"
    LECTURER ="LECTURER" ,"Giảng viên"
    ALUMNI ="ALUMNI","Cựu sinh viên"

class ConfirmStatus(TextChoices):
    PENDING = "Pending", "Chờ xác nhận"
    CONFIRMED = "Confirmed", "Đã xác nhận"
    REJECTED = "Rejected", "Đã từ chối"


class Reaction(TextChoices):
    LIKE = "Like", "Like"
    HAHA = "Haha", "Haha"
    TYM = "Tym", "Thả tym"

class SurveyQuestionType(TextChoices):
    TRAINING_PROGRAM = "Training Program", "Chương trình đào tạo"
    RECRUITMENT_NEEDS = "Recruitment Needs", "Nhu cầu tuyển dụng"
    ALUMNI_INCOME = "Alumni Income", "Thu nhập cựu sinh viên"
    EMPLOYMENT_STATUS = "Employment Status", "Tình hình việc làm"

#Tài khoản
class User(AbstractUser):

    def __str__(self):
        return self.username
#Pass 24h của giảng viên
    # def set_default_password(self):
    #     self.set_password("ou@123")
    #     if self.role == UserRole.LECTURER:  # Áp dụng cho giảng viên
    #         self.force_password_change_deadline = now() + timedelta(hours=24)
    #     else:
    #         self.force_password_change_deadline = None  # Không yêu cầu đổi mật khẩu
    # def is_password_change_required(self):
    #     """Kiểm tra xem có bắt buộc đổi mật khẩu hay không."""
    #     if self.role != UserRole.LECTURER:  # Chỉ kiểm tra cho giảng viên
    #         return False
    #     return self.force_password_change_deadline and now() > self.force_password_change_deadline
#Khi có tài khoản sẽ điền này
class Account(BaseModel):
    avatar = CloudinaryField('avatar',
                             default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1732632586/pfvvxablnkaeqmmbqeit.png",
                             blank=True)
    cover_avatar = CloudinaryField('cover',
                                   default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1733331571/hvyl33kneih3lsn1p9hp.png",
                                   blank=True)
    role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.LECTURER
    )
    account_status = models.BooleanField(default=False) #Để sau 24h không đổi pass thì khóa
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(
        max_length=50,
        choices=Gender.choices,
        default=Gender.Nam
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username
#Fe fetch Api nhớ để ý cái này
    # def get_avatar_url(self):
    #     return self.avatar.url.replace('image/upload/', '')
    #
    # def get_cover_avatar_url(self):
    #     return self.cover_avatar.url.replace('image/upload/', '')


#TK Cựu SV -> primary_key rồi nên nó không có cột id riêng
class AlumniAccount(BaseModel):
    alumni_account_code = models.CharField(max_length=50 ,unique=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE ,primary_key=True)
    #Để quản trị viên xác nhận
    confirm_status = models.CharField(
        max_length=50,
        choices=ConfirmStatus.choices,
        default=ConfirmStatus.PENDING.name
    )

    def __str__(self):
        return self.alumni_account_code

class Post(BaseModel):
    post_content = RichTextField()
    comment_lock = models.BooleanField(default=False)
    account = models.ForeignKey(Account,  on_delete=models.CASCADE, null=True , related_name="posts")
    notification = models.OneToOneField('Notification', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.post_content


#Chi tiết reaction
class PostReaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='post_reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_reactions')
    reaction = models.CharField(
        max_length=50,
        choices=Reaction.choices,
        default=Reaction.LIKE
    )

# #Hình của post
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

# #Post Khảo sát
class PostSurvey(BaseModel):
    post_survey_title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.post_survey_title


# #Câu hỏi
class SurveyQuestion(BaseModel):
    question_content = models.TextField()
    question_order = models.IntegerField()
    is_required = models.BooleanField(default=False)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE ,related_name='survey_questions')
    survey_question_type = models.CharField(
        max_length=50,
        choices=SurveyQuestionType.choices,
        default=SurveyQuestionType.TRAINING_PROGRAM.name
    )
    def __str__(self):
        return self.question_content
# #Lựa chọn
class SurveyQuestionOption(models.Model):
    question_option_value = models.TextField()
    question_option_order = models.IntegerField()
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    survey_answers = models.ManyToManyField('SurveyAnswer', blank=True)

    def __str__(self):
        return self.question_option_value
# #Tra ve KhaoSat
class SurveyResponse(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + ' - ' + self.post_survey.post_survey_title

# #Noi dung cau tra loi
class SurveyAnswer(models.Model):
    answer_value = models.CharField(max_length=1000, null=True, blank=True)
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)

    def __str__(self):
        if not self.answer_value:
            return 'Không có nội dung' + \
                   ' (' + self.survey_question.question_content + ' - ' + self.survey_response.__str__() + ') '
        else:
            return self.answer_value
# # Bài đăng dạng thư mời
class PostInvitation(BaseModel):
    event_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    post = models.OneToOneField(Post , on_delete=models.CASCADE)
    accounts = models.ManyToManyField(Account,blank=True)
# #Lời mời vào nhóm
class InvitationGroup(BaseModel):
    invitation_group_name = models.CharField(max_length=255)
    accounts = models.ManyToManyField(Account, blank=True)

    def __str__(self):
        return self.invitation_group_name
# #Nhóm
class Group(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(Account, related_name='groups', blank=True)

    def __str__(self):
        return self.name

#Thông báo
class Notification(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_sent = models.BooleanField(default=False)
    recipients = models.ManyToManyField(Account, related_name='notifications', blank=True)
    group_recipients = models.ManyToManyField(Group, related_name='notifications', blank=True)

    def __str__(self):
        return self.title

# #Chat 2 người
class Room(BaseModel):
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