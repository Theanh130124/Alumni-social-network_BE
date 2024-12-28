import json
from crypt import methods
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
from django.db import transaction
from django_redis import get_redis_connection #có localhost trong settings host web nhwos chỉnh

redis_connection = get_redis_connection("default")



# post user còn lại dành create admin
class UserViewSet(viewsets.ViewSet , generics.RetrieveAPIView, generics.ListAPIView,  generics.CreateAPIView , generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPageSize
    #http://127.0.0.1:8000/users/?name=Đào -> tìm trên họ tên không nằm trên API này dùng cho thanh tìm kiêm Fe
    def get_queryset(self):
        queryset = self.queryset
        full_name = self.request.query_params.get('full_name')
        if action.__eq__('list'):
            if full_name:
                list_names = full_name.split() #-> tách thành list
                for name in list_names:
                 queryset = queryset.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)) #Có họ ho hoặc tên là được
            return queryset
    def get_permissions(self):
        if self.action in ['list' , 'retrieve', 'create','update','partial_update','current_user','account','create_alumni','create_lecturer']:
            return [permissions.IsAuthenticated()]
        return  [permissions.AllowAny()]

    #Gọi acction bên serializers  -> của thằng khác mới không viết ở đây vd như create_alumni
    def get_serializer_class(self):
        if self.action == 'create': #Gọi vậy thì phải gọi thêm generics.CreateAPIView
            return CreateUserSerializer
        # partial_update -> update khi chỉ cập nhật password
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer

    #current_user
    @action(methods=['get'], url_path='current_user')
    def current_user(self,request):  #request.user -> người dùng htai
        return  Response(UserSerializer(request.user).data,status=status.HTTP_200_OK)

    #Truy vấn ngược -> lấy account dựa trên user id
    @action(methods=['get'], detail=True, url_path='account')
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
    #Phải tạo user trước khi tạo account dưới nên không viet create vào bên serializers được
    @action(methods=['post'],detail=False,url_path='create_alumni')
    def create_alumni(self,request):
        try:
            with transaction.atomic(): #Đảm bảo xảy ra , không thì không lưu
                #Có confirm_status default pending khỏi thêm
                username = request.data.get('username')
                password = request.data.get('password')
                email = request.data.get('email')
                phone_number = request.data.get('phone')
                date_of_birth = request.data.get('date_of_birth')
                avatar = request.data.get('avatar')
                cover = request.data.get('cover')
                first_name = request.data.get('first_name')
                last_name = request.data.get('last_name')
                role = UserRole.ALUMNI
                gender = request.data.get('gender')
                alumni_account_code = request.data.get('alumni_account_code')
                duplicate_username = User.objects.filter(username=username).exists()
                if duplicate_username:
                    return Response({"Username đã tồn tại trong hệ thống": username} , status=status.HTTP_400_BAD_REQUEST)
                duplicate_alumni_account_code = AlumniAccount.objects.filter(alumni_account_code=alumni_account_code).exists()
                if duplicate_alumni_account_code:
                    return Response({"Mã sinh viên đã tồn tại trong hệ thống": username}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(username= username , email=email , first_name=first_name, last_name=last_name ,role=role)
                user.set_password(password)
                user.save()
                account = Account.objects.create(user=user,gender=gender , role=UserRole.ALUMNI.name,  phone_number=phone_number , date_of_birth=date_of_birth , avatar=avatar , cover=cover )
                alumni = AlumniAccount.objects.create(account=account,alumni_account_code=alumni_account_code )
                return  Response(AlumniAccountSerializer(alumni).data,status=status.HTTP_200_OK)
            # except IntegrityError as e:
            #     error_message = str(e)
            #     return Response({'Trùng khóa chính: ': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            return Response({'Phát hiện lỗi: ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(methods=['post'], detail=False , url_path='create_lecturer')
    def create_lecturer(self ,request):
        try:
            with transaction.atomic():
                username = request.data.get('username')
                #Password ou@123
                email = request.data.get('email')
                first_name = request.data.get('first_name')
                last_name = request.data.get('last_name')
                phone_number = request.data.get('phone')
                date_of_birth = request.data.get('date_of_birth')
                avatar = request.data.get('avatar')
                cover = request.data.get('cover')
                gender = request.data.get('gender')
                # role = UserRole.LECTURER default rồi
                duplicate_username = User.objects.filter(username=username).exists()
                if duplicate_username:
                    return Response({"Username đã tồn tại trong hệ thống": username} , status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(username=username,email=email  ,first_name = first_name ,last_name = last_name)
                user.set_password('ou@123')
                user.save()
                account = Account.objects.create(user=user , gender = gender , phone_number=phone_number , date_of_birth=date_of_birth ,avatar=avatar,cover=cover)
                return Response(AccountSerializer(account).data , status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'Phát hiện lỗi: ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Tìm kiếm gần đây
    @action(methods=['get'] , url_path='recent_search')
    def recent_search(self, request):
        try:
            full_name = self.request.query_params.get('full_name')
            cached_data = redis_connection.get(full_name if full_name is None else '')
            if cached_data:
                #json.loads -> python (dictionary)
                data = json.loads(cached_data)
                return Response(data, status=status.HTTP_200_OK)
            user = User.objects.all()
            if full_name:
                names = full_name.split()
                for name in names:
                    user = user.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) ,ex=3600) #1 giờ
                    account = Account.objects.filter(user__in=user)
                    #Chuyển dữ liệu thành str Json để lưu bằng dumps
                    redis_connection.set(full_name,json.dumps(AccountSerializer(account,many=True),status=status.HTTP_200_OK))
        except Exception as ex:
            return Response({'Phát hiện lỗi': str(ex)} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    #Khác với get_params ở trên là cái này lấy account trong hệ thống
    @action(methods=['get'] ,url_path='search_account')
    def search_account(self,request):
        try:
            full_name = self.request.query_params.get('full_name')
            user = User.objects.all()
            #Xem xét lại tìm kiếm mấy tài khoản bị khóa 


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

