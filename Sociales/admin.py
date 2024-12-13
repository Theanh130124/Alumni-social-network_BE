from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField


class SocialMediaAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG MẠNG XÃ HỘI CỰU SV TRỰC TUYẾN'
    index_title = 'Thế Anh DjangonAdministration'

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username','email', 'confirm_status']
    search_fields = ['username']
    list_filter = ['confirm_status']
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user' , 'role', 'account_status','phone_number']
    search_fields =  ['role','user','phone_number']
    list_filter = ['role']
class AlumniAccountAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'alumni_account_code']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_content', 'comment_lock', 'account']
    search_fields = ['post_content', 'account']
    list_filter = ['comment_lock']
    # inline  -> nữa thêm PostImage .....
class ReactionAdmin(admin.ModelAdmin):
    list_filter = ['reaction_name']


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
    list_display = ['id', 'post_survey_title', 'start_time', 'end_time', 'is_closed', 'post']
    search_fields = ['post_survey_title']
    inlines = [SurveyQuestionInLineAdmin]


class SurveyQuestionTypeAdmin(admin.ModelAdmin):
    pass


class SurveyQuestionOptionInLineAdmin(admin.TabularInline):
    model = SurveyQuestionOption

my_admin_site = SocialMediaAppAdminSite(name='TheAnhAdmin')
my_admin_site.register(User,UserAdmin)
my_admin_site.register(Account,AccountAdmin)
my_admin_site.register(AlumniAccount,AlumniAccountAdmin)
my_admin_site.register(Post, PostAdmin)
my_admin_site.register(Reaction,ReactionAdmin)
my_admin_site.register(PostReaction,PostReactionAdmin)
my_admin_site.register(PostImage, PostImageAdmin)
my_admin_site.register(Comment, CommentAdmin)
my_admin_site.register(PostSurvey, PostSurveyAdmin)
my_admin_site.register(SurveyQuestionType, SurveyQuestionTypeAdmin)

