import json

from dbm import error
from re import search


from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets , generics , permissions ,status
from rest_framework.decorators import action, api_view
from Sociales.models  import *
from .paginators import MyPageSize
from .serializers import *
from .swagger_decorators import *
from django.db import transaction
from rest_framework.exceptions import NotFound
from django_redis import get_redis_connection #có localhost trong settings host web nhwos chỉnh

redis_connection = get_redis_connection("default")



class EnumCollectionView(APIView):
    def get(self, request):
        serializer = EnumCollectionSerializer()
        return Response(serializer.data)

#InvitationGroup
@method_decorator(decorator=header_authorization, name='list')
@method_decorator(decorator=header_authorization, name='create')
@method_decorator(decorator=header_authorization, name='retrieve')
@method_decorator(decorator=header_authorization, name='update')
@method_decorator(decorator=header_authorization, name='partial_update')
@method_decorator(decorator=header_authorization, name='destroy')
class InvitationGroupViewSet(viewsets.ViewSet, generics.ListAPIView , generics.RetrieveAPIView, generics.CreateAPIView,generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = InvitationGroup.objects.filter(active=True)
    serializer_class = InvitationGroupSerializer
    pagination_class = MyPageSize
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action =='create':
            return  CrateInvitationGroupSerializer
        if self.action in ['update','partial_update']:
            return UpdateInvitationGroupSerializer
        if self.action == 'retrieve':
            return  0  ###

    @action(methods=['GET'], detail=True, url_path='accounts')
    @method_decorator(decorator=header_authorization,name='accounts')
    def get_accounts(self,request,pk):
        try:
            accounts = self.get_object().accounts.filter(active=True).all()
            paginator =MyPageSize()
            paginated = paginator.paginate_queryset(accounts,request)
            serializer = AccountSerializerForInvitationGroup(paginated, many=True,context={'request':request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'Phát hiện lỗi ': error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail =True, url_path='add_or_update_accounts')
    @method_decorator(decorator=add_or_update_accounts_from_invitation_group, name='add_or_update_accounts')
    def add_or_update_accounts(self, request , pk):
        try:
            with transaction.atomic(): #Error -> thì rollback (về trang thái trước)
                invitation_group = self.get_object()
                list_account_id = request.data.get('list_account_id',[])
                list_account_id =set(list_account_id) #set loại dữ liệu trùng
                accounts = Account.objects.filter(id__in=list_account_id)
                if len(accounts) != len(list_account_id):
                    missing_ids = set(list_account_id) - set(accounts.values_list('id', flat=True))
                    raise NotFound(f'Accounts với IDs {missing_ids} không tồn tại.')
                invitation_group.accounts.remove(*accounts)
                invitation_group.save()

                return Response(InvitationGroupSerializer(invitation_group).data , status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":str (e)} ,status =status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(methods=['GET'], detail=False , url_path ='search_group_cache')
    @method_decorator(decorator=search_invitation_group_cache, name ='search_group_cache')
    def search_group_cache(self,request):
        try:
            invitation_group_name = self.request.query_params.get('invitation_group_name')
            cached_data  = redis_connection.get('search_group_cache:'+invitation_group_name if invitation_group_name is not None else "")
            print("Đây là dữ liệu từ redis")
            print(cached_data)
            if cached_data:
                return  Response(json.loads(cached_data) , status=status.HTTP_200_OK)
            invitation_groups = InvitationGroup.objects.filter(invitation_group_name__icontains=invitation_group_name)
            print(invitation_groups)
            data = []
            for group in invitation_groups:
                group_data = InvitationGroupSerializer(group).data
                accounts = group.accounts.all()
                accounts_data = AccountSerializerForUser(accounts,many=True).data
                group_data['accounts_info'] = accounts_data
                data.append(group_data)
                print(accounts)
            print(data)
            redis_connection.set('search_group_cache:'+invitation_group_name, json.dumps(data) , ex=300)
            return Response(data , status=status.HTTP_200_OK)
        except Exception as e :
            error_message = str(e)
            return Response({'Phát hiện lỗi ': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

