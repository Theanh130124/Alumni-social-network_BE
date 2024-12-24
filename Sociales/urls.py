from rest_framework import  routers
from django.contrib.auth.views import  LoginView , LogoutView
from  .views import  *
from django.urls import path, re_path, include
router  = routers.DefaultRouter()
#Tách ra quản lý ?
router.register('enumcollection', EnumCollectionView , basename='enumcollection')
router.register('invitation_groups', InvitationGroupViewSet , basename ='invitation_groups')


app_name = 'app'

urlpatterns = [
    path('',include(router.urls)),
    ]