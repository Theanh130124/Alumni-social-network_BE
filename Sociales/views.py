from crypt import methods
from dbm import error

from django.contrib.admin import action
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets , generics , permissions ,status
from Sociales.models  import *
from .paginators import MyPageSize
from .serializers import *
from .swagger_decorators import *


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
    
