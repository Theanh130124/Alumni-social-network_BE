
from rest_framework import  routers
from django.contrib.auth.views import  LoginView , LogoutView
from  .views import  *
from django.urls import path, re_path, include
router  = routers.DefaultRouter()

router.register('users',UserViewSet,basename='users')
router.register('accounts',AccountViewSet,basename='accounts')
router.register('alumni-accounts',AlumniAccountViewSet,basename='alumni-accounts')


urlpatterns = [
    path('',include(router.urls)),
    ]