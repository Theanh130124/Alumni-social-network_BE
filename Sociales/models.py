from datetime import datetime

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import default


class BaseModel(models.Model):
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Roles(models.TextChoices):
    FORMER = 'FORMER_STUDENT' ,'Cựu học sinh'
    LECTURER = 'LECTURER', 'Giảng viên'
    ADMIN = 'ADMIN', 'Quản trị viên'
class Gender(models.TextChoices):
    MALE = 'True', 'Nam'
    FEMALE = 'False','Nữ'

class AccountStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Hoạt động'
    INACTIVE = 'INACTIVE', 'Không hoạt động'
    SUSPENDED = 'SUSPENDED', 'Bị khóa'

class Profile(models.Model):
    user = models.OneToOneField('User',on_delete=models.SET_NULL , null= True , blank = True) #Xóa User -> Profile vẫn còn -> user_id = null
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50) #Trong user có
    address = models.TextField()
    birthday = models.DateField(default=datetime.now())
    phone_number = models.CharField(max_length=10)
    # email = models.CharField(max_length=255, unique=True)
    gender = models.BooleanField(choices=Gender.choices, default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
class User(AbstractUser):
    role = models.CharField(choices=Roles.choices , max_length=50)
    avatar_user = CloudinaryField('avatar', blank=True, default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1732632586/pfvvxablnkaeqmmbqeit.png")
    cover_photo = CloudinaryField('cover', blank=True, default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1733331571/hvyl33kneih3lsn1p9hp.png")
    # Trạng thái hđ
    account_status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.INACTIVE)
class Comment(models.Model):
    pass
class Like(models.Model):
    pass
class Post():
    pass


class test123:
    




