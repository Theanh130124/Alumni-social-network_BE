from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import default
from django.db.models import TextChoices
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.utils.html import strip_tags

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
    password_changed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username

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
    account_status = models.BooleanField(default=True) #Để sau 24h không đổi pass thì khóa
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
    #Viết toString để bên admin thấy
    def __str__(self):
        return self.alumni_account_code

class Post(BaseModel):
    post_content = RichTextField()
    comment_lock = models.BooleanField(default=False)
    account = models.ForeignKey(Account,  on_delete=models.CASCADE, null=True , related_name="posts")

    def __str__(self):
        return self.post_content
    def save(self, *args, **kwargs):
        # Loại bỏ thẻ HTML khỏi nội dung trước khi lưu
        self.post_content = strip_tags(self.post_content)
        super().save(*args, **kwargs)


#Chi tiết reaction
class PostReaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='post_reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_reactions')
    reaction = models.CharField(
        max_length=50,
        choices=Reaction.choices,
        default=Reaction.LIKE
    )
    class Meta:
        unique_together = ('account','post') #Chỉ thả 1 reaction trên 1 post

# #Hình của post tách ra vì 1 bài viết có nhiều hình ảnh 
class PostImage(BaseModel):
    post_image_url = CloudinaryField(blank=True , null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='post_images')

    def __str__(self):
        return f'https://res.cloudinary.com/dxiawzgnz/{self.post_image_url}'


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
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
#-> Validate việc lúc tạo còn lúc update validate bên view
    def clean(self):
        # Kiểm tra nếu end_time nhỏ hơn start_time
        if self.end_time < self.start_time:
            raise ValidationError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu .")
    def __str__(self):
        return self.post_survey_title


# #Câu hỏi ở trên đầu -> vd : OOp là gì ?
class SurveyQuestion(BaseModel):
    question_content = models.TextField()
    question_order = models.IntegerField()
    is_required = models.BooleanField(default=False) #bắt buoc trả lời
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE ,related_name='survey_questions')
    survey_question_type = models.CharField(
        max_length=50,
        choices=SurveyQuestionType.choices,
        default=SurveyQuestionType.TRAINING_PROGRAM.name
    )
    def __str__(self):
        return self.question_content
#Trả lời cho các câu hỏi trắc nghiệm
class SurveyQuestionOption(models.Model):
    question_option_value = models.TextField() #A.Open objects p  B...  C... D
    question_option_order = models.IntegerField()#1 , 2 ,3 ,4
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE) #->thuoc cau hỏi
    survey_answers = models.ManyToManyField('SurveyAnswer', blank=True)

    def __str__(self):
        return self.question_option_value
#Trả về để xem người đó đã làm khảo sát chưa -> tính tỉ lệ người hoàn thành
class SurveyResponse(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post_survey = models.ForeignKey(PostSurvey, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + ' - ' + self.post_survey.post_survey_title

#Câu trả lời dành cho các câu tự luận
class SurveyAnswer(models.Model):
    answer_value = models.CharField(max_length=1000, null=True, blank=True) #Trả lời 1 câu
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
    post = models.OneToOneField(Post , on_delete=models.CASCADE) ##Chổ này có post_id nhá
    accounts_alumni = models.ManyToManyField(AlumniAccount,blank=True) #-> Xem ở đâu có nên đổi AlumniAccount không
# #Lời mời vào nhóm
class InvitationGroup(BaseModel):
    invitation_group_name = models.CharField(max_length=255)
    accounts = models.ManyToManyField(Account, blank=True)

    def __str__(self):
        return self.invitation_group_name
# #Nhóm
class Group(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(Account, related_name='groups', blank=True) # Tha tu dau de AlumniAccount

    def __str__(self):
        return self.name


# #Chat 2 người
class Room(BaseModel):
    first_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='first_user_room', null=True)
    second_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='second_user_room', null=True)


    class Meta:
        unique_together = ['first_user', 'second_user']

    def __str__(self):
        return f'Đoạn này này của'+str(self.first_user.user.username)+f'và'+str( self.second_user.user.username) #Viết toString để bên admin thấy


class Message(BaseModel):
    who_sent = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)  # Người gửi
    content = models.CharField(max_length=10000)  # Nội dung tin nhắn
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)  # Phòng chat
    seen = models.BooleanField(default=False)  # Trạng thái đã xem
    timestamp = models.DateTimeField(default=timezone.now)  # Thời gian gửi tin nhắn

    def __str__(self):
        return f"Message from {self.who_sent} in room {self.room} at {self.timestamp}"

#Ở FILE NÀY MESSAGE CHƯA ĐC MIGRATIONS VÌ LƯỜI XÓA ;)
