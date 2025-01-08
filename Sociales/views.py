import json
from asyncio import Future


from functools import partial
from lib2to3.fixes.fix_input import context
from multiprocessing.reduction import duplicate
from pickle import FALSE

import cloudinary.uploader
from cloudinary.cache.responsive_breakpoints_cache import instance
from cloudinary.uploader import upload
from django.contrib.admin.templatetags.admin_list import pagination
from django.core.exceptions import ObjectDoesNotExist
from dbm import error
from re import search
from django.db.models import Count, Q
from django.db.models.functions import TruncYear
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.template.defaultfilters import first
from django.utils.decorators import method_decorator
from rest_framework import viewsets , generics , permissions ,status ,parsers
from rest_framework.decorators import action, api_view
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from Sociales.models  import *
from .paginators import MyPageSize, MyPageListReaction
from .serializers import *
from django.db import transaction
from django_redis import get_redis_connection #có localhost trong settings host web nhwos chỉnh

redis_connection = get_redis_connection("default")



#Chỉ cần truyền fields = ['','']
class FileUploadHelper:
    @staticmethod
    def upload_files(request , fields):
        try:
            upload_res = {}
            for field in fields:
                file = request.data.get(field)
                if file:
                    upload_res[field]=cloudinary.uploader.upload(file)['secure_url']
            return upload_res
        except Exception as ex:
            raise Exception(f'Phát hiện lỗi : {str(ex)}')
#



# post user còn lại dành create admin
class UserViewSet(viewsets.ViewSet , generics.RetrieveAPIView, generics.ListAPIView,  generics.CreateAPIView , generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPageSize
    parser_classes = [parsers.MultiPartParser] # De upload FIle
    #http://127.0.0.1:8000/users/?full_name=Đào -> tìm trên họ tên không nằm trên API này dùng cho thanh tìm kiêm Fe
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
        if self.action.__eq__('create_lecturer'):#do admin tạo lecturer
            return [IsAdminUserRole()]
        if self.action in ['list' , 'retrieve' ,'update','partial_update','current_user','account' ,'search_account','recent_search']:
            return [permissions.IsAuthenticated()]
        return  [permissions.AllowAny()] #'create_alumni' .... ngta đk đc

    #Gọi acction bên serializers  -> của thằng khác mới không viết ở đây vd như create_alumni
    def get_serializer_class(self):
        if self.action == 'create': #Gọi vậy thì phải gọi thêm generics.CreateAPIView
            return CreateUserSerializer
        # partial_update -> update khi chỉ cập nhật password
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer

    #current_user
    @action(methods=['get'],detail=False, url_path='current_user')
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
    #Bật detail true được truyền id vào
    @action(methods=['post'],detail=False,url_path='create_alumni')
    def create_alumni(self,request):
        try:
            # Xem coi ngày tạo với ngày update
            with transaction.atomic(): #Đảm bảo xảy ra , không thì không lưu
                #Có confirm_status default pending khỏi thêm
                username = request.data.get('username')
                password = request.data.get('password')
                email = request.data.get('email')
                phone_number = request.data.get('phone')
                date_of_birth = request.data.get('date_of_birth')
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
                user = User.objects.create_user(username= username , email=email , first_name=first_name, last_name=last_name )
                user.set_password(password)
                user.save()
                account = Account.objects.create(user=user,gender=gender , role=UserRole.ALUMNI.name,  phone_number=phone_number , date_of_birth=date_of_birth  )
                alumni = AlumniAccount.objects.create(account=account,alumni_account_code=alumni_account_code )
                return  Response(AlumniAccountSerializer(alumni).data,status=status.HTTP_200_OK)
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
                gender = request.data.get('gender')
                # role = UserRole.LECTURER default rồi
                duplicate_username = User.objects.filter(username=username).exists()
                if duplicate_username:
                    return Response({"Username đã tồn tại trong hệ thống": username} , status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(username=username,email=email  ,first_name = first_name ,last_name = last_name)
                user.set_password('ou@123')
                user.save()
                account = Account.objects.create(user=user , gender = gender , phone_number=phone_number , date_of_birth=date_of_birth )
                return Response(AccountSerializer(account).data , status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({'Phát hiện lỗi: ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Tìm kiếm gần đây  -> de fix sau
    @action(methods=['get'] , detail=False,url_path='recent_search')
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
    @action(methods=['get'] , detail=False ,url_path='search_account')
    def search_account(self,request):
        try:
            full_name = self.request.query_params.get('full_name')
            user = User.objects.all()
            if full_name:
                names = full_name.split()
                for name in names:
                    user = user.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
                    account = Account.objects.filter(user__in=user)
                    #Xem coi co nen tach ra thanh UserSerializerForSearch khong ?
            else:
                account = Account.objects.none()
            return Response(AccountSerializer(account, many=True).data, status=status.HTTP_200_OK)
        except Exception as ex :
            return Response({'Phát hiện lỗi': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AccountViewSet( viewsets.ViewSet ,generics.ListAPIView,generics.UpdateAPIView):
    queryset = Account.objects.all() #Xem nếu filter comfirm_status ?
    serializer_class = AccountSerializer
    pagination_class = MyPageSize
    parser_classes = [parsers.MultiPartParser]# De upload FIle thì dùng

    def get_permissions(self):
        if self.action in ['list' ,'update' , 'partial_update','get_post_of_account']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_update(self, serializer):
        fields = ['avatar','cover_avatar']
        upload_res = FileUploadHelper.upload_files(self.request,fields=fields)
        serializer.save(**upload_res)

    def update(self, request, *args, **kwargs):
        return super().update(request,*args,**kwargs)

    #Xem những bài viết của accout đó
    @action(methods=['get'],detail=True,url_path='post')
    def get_post_of_account(self,request,pk):
        try:
            posts = self.get_object().posts.filter(active=True).order_by('-created_date').all() #do có related_name rồi
            paginator = MyPageSize()
            paginated = paginator.paginate_queryset(posts, request)
            return Response(PostSerializer(paginated,many=True,context={'request':request}).data,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'Phát hiện lỗi',str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update trạng thái đăng nhập từ admin cho cựu sv
class AlumniAccountViewSet(viewsets.ViewSet ,generics.ListAPIView , generics.RetrieveAPIView,generics.UpdateAPIView):
    queryset = AlumniAccount.objects.all()
    serializer_class = AlumniAccountSerializer
    pagination_class = MyPageSize

    def get_permissions(self):
        if self.action in ['list' ,'update' , 'partial_update', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class PostViewSet(viewsets.ViewSet,generics.ListAPIView, generics.CreateAPIView , generics.RetrieveAPIView , generics.UpdateAPIView , generics.DestroyAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostSerializer
  #Truyền vào do có tự định nghĩa PostOwner
    pagination_class =  MyPageSize



    def get_serializer_class(self):
        if self.action.__eq__('create'):
            return CreatePostSerializer
        return PostSerializer
    def get_permissions(self):
        if self.action in ['destroy','update','partial_update']:
            return [PostOwner()]
        if  self.action in ['list','retrieve','create','get_comments_in_post','get_image_in_post','get_reaction_detail_in_post',
                            ]:
            return [permissions.IsAuthenticated()]
        return  [permissions.AllowAny()]
    @action(methods=['get'] , detail=True,url_path='comments')
    def get_comments_in_post(self,request,pk):
        try:
            #get_querryset().get(pk=pk) sẽ lấy được bài viết theo pk còn get_object thì không
            comments = self.get_queryset().get(pk=pk).comments.filter(active=True).order_by('-created_date').all() #có khai báo related_name rồi
            paginator = MyPageSize()
            paginated = paginator.paginate_queryset(comments, request)
            serializer = CommentSerializer(paginated, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as ex:
            return Response({'Phát hiện lỗi',str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#lấy các hình ảnh của bài viết
    @action(methods=['get'],detail=True,url_path='images')
    def get_image_in_post(self,request,pk):
        try:
            post_images =self.get_queryset().get(pk=pk).post_images.filter(active=True).all()
            paginator = MyPageSize()
            paginated = paginator.paginate_queryset(post_images,request)
            serializer = PostImageSerializer(paginated,many=True,context={'request':request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as ex:
            return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#lấy reaction -> nếu không truyền parames nào thì nó sẽ không hiện parmes đó -> đồng thời có thể lọc reaction
    @action(methods=['get'],detail=True,url_path='reactions')
    def get_reaction_detail_in_post(self,request,pk):
        try:
            reaction = request.query_params.get('reaction')
            account_id = request.query_params.get('account')
            post_reactions = PostReaction.objects.filter(post_id=pk) #Nếu không truyền parames gì thì nó hiện list reaction thôi
            if reaction :
                 post_reactions = post_reactions.filter(reaction=reaction)
            if account_id:
                post_reactions = post_reactions.filter(account_id=account_id)
            paginator = MyPageListReaction()
            paginated = paginator.paginate_queryset(post_reactions, request)
            return Response(PostReactionSerializer(paginated,many=True,context={'request':request}).data,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# #Dem tat ca reaction tren 1 post
#     @action(methods=['get'],detail=True,url_path='count_reaction')
#     def get_count_reaction(self,request,pk):
#         try:
#             reaction_count = PostReaction.objects.filter(post_id=pk).count()
#             return Response(reaction_count,status=status.HTTP_200_OK)
#         except Exception as ex:
#             return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #Lấy loại cảm xúc trên 1 bài viết
#     @action(methods=['get'],detail=True,url_path="count_type_reaction")
#     def get_count_type_reaction(self,request,pk):
#         try:
#             #annotate -> truyền id để nó đếm số lượng theo id -> nếu 1 post có nhiều postreaction có thể dùng annostate để đếm cảm xúc
#             reaction_type = PostReaction.objects.filter(post_id=pk).annotate(count=Count('id')).values('reaction','count')
#             return Response(reaction_type,status=status.HTTP_200_OK)
#         except Exception as ex:
#             return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             #values -> chọn thuộc tính lấy
# #dem so binh luan
#     @action(methods=['get'],detail=True,url_path="count_comment")
#     def get_count_comment(self,request,pk):
#         try:
#             count_comment = Comment.objects.filter(post_id=pk).count()
#             return Response(count_comment,status=status.HTTP_200_OK)
#         except Exception as ex:
#             return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#Tối ưu bằng gộp và dùng annotate để group_by -> để chia các reaction có cùng post_id -> thành 1 group_by reaction -> từng loại riêng với count từng loại
    def retrieve(self, request, *args, **kwargs):
        try:
            post =self.get_object()
            comment_count = Comment.objects.filter(post_id = post.id).count()
            #Đến từng loại cảm xúc -> kèm theo số lượng
            reactions =PostReaction.objects.filter(post_id=post.id).annotate(count=Count('reaction')).values('reaction','count') #ở đây nó truyền account thì nó sẽ đếm theo account ,
            total_reactions = PostReaction.objects.filter(post_id=post.id).count()
            serializer = self.get_serializer(post)
            data = serializer.data
            data['comment_count'] =comment_count
            data['reactions'] = reactions
            data['total_reactions'] = total_reactions
            return Response(data,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'Phát hiện lỗi', str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Post -> Việc xử lý Thả cảm xúc , và hủy
class PostReactionViewSet(viewsets.ViewSet,generics.CreateAPIView,generics.DestroyAPIView ,generics.UpdateAPIView):
    queryset = PostReaction.objects.all()
    serializer_class =  PostReactionSerializer
    pagination_class =  MyPageSize

    def get_permissions(self):
        if self.action in ['partial_update','destroy']:
            return [PostReactionOwner()]
        else: 
            return [permissions.IsAuthenticated()]
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return PostReactionForCreateUpdateSerializer
        return self.serializer_class
#Create
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            account = request.user.account
            post = serializer.validated_data['post'] #lấy post bên serializer
            existing_reaction = PostReaction.objects.filter(account=account,post=post) #Kiểm tra có trùng cảm xúc không
            if existing_reaction: #Có thì parse qua bên serializers vào reaction
                 existing_reaction.reaction = serializer.validated_data['reaction']
                 existing_reaction.save()
                 return Response(self.get_serializer(existing_reaction).data, status=status.HTTP_200_OK)
            else:
                serializer.save(account=account)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Sửa lại cảm xúc
    def partial_update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                # Cập nhật cảm xúc
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Xóa cả xúc -> nhấn đúp
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Lấy đối tượng cần xóa
        instance.delete()  # Xóa đối tượng
        return Response(status=status.HTTP_204_NO_CONTENT)


