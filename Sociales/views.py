import json
from multiprocessing.reduction import duplicate

from django.core.exceptions import ObjectDoesNotExist
from dbm import error
from re import search
from django.db.models import Count, Q

from django.shortcuts import render
from django.template.defaultfilters import first
from django.utils.decorators import method_decorator
from rest_framework import viewsets , generics , permissions ,status
from rest_framework.decorators import action, api_view
from rest_framework.viewsets import ModelViewSet

from Sociales.models  import *
from .paginators import MyPageSize
from .serializers import *
from .swagger_decorators import *
from django.db import transaction
from rest_framework.exceptions import NotFound
from django_redis import get_redis_connection #có localhost trong settings host web nhwos chỉnh

redis_connection = get_redis_connection("default")


class UserViewSet(viewsets.ViewSet , generics.RetrieveAPIView, generics.ListAPIView,  generics.CreateAPIView , generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPageSize
    #http://127.0.0.1:8000/users/?name=Đào -> tìm trên họ tên không nằm trên API
    def get_queryset(self):
        queries = self.queryset
        name = self.request.query_params.get('name')
        if name:
            names = name.split()
            for name in names:
                queries =queries.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        return queries
    # def get_permissions(self):
    #     if self.action in ['']
    #         return [permissions.IsAuthenticated()]
    #     return  [permissions.AllowAny()]

    #Create , update
    def get_serializer_class(self):
        if self.action == 'create': #Gọi vậy thì phải gọi thêm generics.CreateAPIView
            return CreateUserSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer

    #current_user
    @action(methods=['get'],detail=False , url_path='current_user')
    def current_user(self,request):
        return  Response(UserSerializer(request.user).data,status=status.HTTP_200_OK)

    #Truy vấn ngược
    @action(methods=['get'], detail=True, url_path='get_account_by_user_id')
    def get_account_by_user_id(self,request,pk):
        try:
            user = self.get_object()
            account = user.account
            return Response(AccountSerializer(account,context={'request':request}).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Tài khoản không tồn tại!!!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = str(e)
            return Response({'Lỗi : ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'],detail=False,url_path='create_alumni')
    def create_alumni(self,request):
        try: #Xem còn sđt ,avt , cover
            with transaction.atomic(): #Đảm bảo xảy ra , không thì không lưu
                username = request.data.get('username')
                password = request.data.get('password')
                email = request.data.get('email')
                first_name = request.data.get('first_name')
                last_name = request.data.get('last_name')
                gender = request.data.get('gender')
                alumni_account_code = request.data.get('alumni_account_code')
                duplicate_username = User.objects.filter(username=username).exists()
                if duplicate_username:
                    return Response({"Username đã tồn tại trong hệ thống": username} , status=status.HTTP_400_BAD_REQUEST)
                duplicate_alumni_account_code = AlumniAccount.objects.filter(alumni_account_code=alumni_account_code).exists()
                if duplicate_alumni_account_code:
                    return Response({"Mã sinh viên đã tồn tại trong hệ thống": username}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(username= username , email=email , first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                account = Account.objects.create(user=user,gender=gender , role=UserRole.ALUMNI.name)
                alumni = AlumniAccount.objects.create(account=account,alumni_account_code=alumni_account_code)
                return  Response(AlumniAccountSerializer(alumni).data,status=status.HTTP_200_OK)
            # except IntegrityError as e:
            #     error_message = str(e)
            #     return Response({'Trùng khóa chính: ': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            return Response({'Phát hiện lỗi: ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AccountViewSet(viewsets.ViewSet ,generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

  # # Override lại để dùng cái Serializer create, update
  #   def get_serializer_class(self):
  #       if self.action == 'create':
  #           return CreateUserSerializer
  #       if self.action in ['update', 'partial_update']:
  #           return UpdateUserSerializer
  #       return self.serializer_class

class AlumniAccountViewSet(viewsets.ViewSet ,generics.ListAPIView):
    queryset = AlumniAccount.objects.all()
    serializer_class = AlumniAccountSerializer

