
from rest_framework import  routers
from django.contrib.auth.views import  LoginView , LogoutView
from  .views import  *
from django.urls import path, re_path, include
router  = routers.DefaultRouter()

router.register('users',UserViewSet,basename='users') #basename dùng trên FE
router.register('accounts',AccountViewSet,basename='accounts')
router.register('alumni_accounts',AlumniAccountViewSet,basename='alumni_accounts')
router.register('post',PostViewSet,basename='post')
router.register('post_reaction',PostReactionViewSet,basename='post_reaction')

urlpatterns = [
    path('',include(router.urls)),
    ]