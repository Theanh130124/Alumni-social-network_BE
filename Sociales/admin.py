from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField


class SocialMediaAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG MẠNG XÃ HỘI CỰU SV TRỰC TUYẾN'
    index_title = 'Thế Anh DjangonAdministration'

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name','last_name','email']
    search_fields = ['username', 'role']


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user' ,'phone_number' ,'role',]
    search_fields =  ['user','phone_number' ,'role',]
    list_filter = ['role']

class AlumniAccountAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'alumni_account_code' ,'confirm_status']
    list_filter = ['confirm_status']

class PostImageAdminInLine(admin.TabularInline):
    model = PostImage
    extra = 1 #Cho chose 1 ảnh cho đỡ rối mắt
class CommentAdminInLine(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_content', 'comment_lock', 'account']
    search_fields = ['post_content', 'account']
    list_filter = ['comment_lock']
    inlines = [PostImageAdminInLine,CommentAdminInLine]

class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'post', 'reaction', 'account']


class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_image_url', 'post_id']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_id', 'comment_content', 'comment_image_url', 'post_id']
    search_fields = ['comment_content']


class SurveyQuestionInLineAdmin(admin.TabularInline):
    model = SurveyQuestion


class PostSurveyAdmin(admin.ModelAdmin):
    list_display = [ 'post_survey_title', 'start_time', 'end_time', 'is_closed', 'post']
    search_fields = ['post_survey_title']
    inlines = [SurveyQuestionInLineAdmin]

class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['survey_question_type']

class SurveyQuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['survey_question']

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['account','post_survey']
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_value','survey_question']
class PostInvitationAdmin(admin.ModelAdmin):
    list_display = ['event_name']
class InvitationGroupAdmin(admin.ModelAdmin):
    list_display = ['invitation_group_name']
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['first_user','second_user']
class MessageAdmin(admin.ModelAdmin):
    list_display = ['who_sent','room']


my_admin_site = SocialMediaAppAdminSite(name='TheAnhAdmin')
my_admin_site.register(User,UserAdmin)
my_admin_site.register(Account,AccountAdmin)
my_admin_site.register(AlumniAccount,AlumniAccountAdmin)
my_admin_site.register(Post, PostAdmin)
my_admin_site.register(PostReaction,PostReactionAdmin)
my_admin_site.register(PostImage, PostImageAdmin)
my_admin_site.register(Comment, CommentAdmin)
my_admin_site.register(PostSurvey, PostSurveyAdmin)
my_admin_site.register(SurveyQuestion,SurveyQuestionAdmin)
my_admin_site.register(SurveyQuestionOption,SurveyQuestionOptionAdmin)
my_admin_site.register(SurveyResponse,SurveyResponseAdmin)
my_admin_site.register(SurveyAnswer,SurveyAnswerAdmin)
my_admin_site.register(PostInvitation,PostInvitationAdmin)
my_admin_site.register(InvitationGroup,InvitationGroupAdmin)
my_admin_site.register(Group,GroupAdmin)

my_admin_site.register(Room,RoomAdmin)
my_admin_site.register(Message,MessageAdmin)

from django_celery_beat.models import PeriodicTask, IntervalSchedule, ClockedSchedule, SolarSchedule, CrontabSchedule, \
    PeriodicTasks

my_admin_site.register(PeriodicTask)
my_admin_site.register(IntervalSchedule)
my_admin_site.register(ClockedSchedule)
my_admin_site.register(SolarSchedule)
my_admin_site.register(CrontabSchedule)
my_admin_site.register(PeriodicTasks)

from django_celery_results.models import TaskResult, GroupResult
my_admin_site.register(TaskResult)
my_admin_site.register(GroupResult)

# from Sociales.models import UserSocialAuth, Association, Code, Nonce, Partial
# my_admin_site.register(UserSocialAuth)
# my_admin_site.register(Association)
# my_admin_site.register(Code)
# my_admin_site.register(Nonce)
# my_admin_site.register(Partial)


