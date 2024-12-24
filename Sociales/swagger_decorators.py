# from django.contrib.messages import warning
#
# #Infomation cho người dùng khi dùng API
# from .serializers import *
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
#
# header_authorization = swagger_auto_schema(
#     manual_parameters=[
#         openapi.Parameter(
#             name='Authorization',
#             in_=openapi.IN_HEADER,
#             type=openapi.TYPE_STRING,
#             description='Token for authentication (Thêm Bearer )',
#             required=True
#         )
#     ],
#     order=['Authorization', 'header']
# )
# add_or_update_accounts_from_invitation_group = swagger_auto_schema(
#     manual_parameters=[
#         openapi.Parameter(
#             name='Authorization',
#             in_=openapi.IN_HEADER,
#             type=openapi.TYPE_STRING,
#             description='Token for authentication (Thêm Bearer )',
#             required=True
#         )
#     ],
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'list_account_id': openapi.Schema(
#                 type=openapi.TYPE_ARRAY,
#                 items=openapi.Schema(type=openapi.TYPE_INTEGER),
#                 description='List of account IDs',
#                 example=[1, 2, 3]
#             ),
#         },
#         required=['list_account_id'],
#     ),
#     responses={
#         status.HTTP_201_CREATED: openapi.Response(
#             description='Success',
#             schema=InvitationGroupSerializer,
#         ),
#         status.HTTP_400_BAD_REQUEST: openapi.Response(
#             description='Bad request',
#         ),
#         status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
#             description='Internal server error',
#         ),
#     }
# )
# search_invitation_group_cache = swagger_auto_schema(
#     manual_parameters=[
#         openapi.Parameter(
#             name='Authorization',
#             in_=openapi.IN_HEADER,
#             type=openapi.TYPE_STRING,
#             description='Token for authentication ( thêm Bearer)',
#             required=True
#         ),
#         openapi.Parameter(
#             name='invitation_group_name',
#             in_=openapi.IN_QUERY,
#             description='Invitation Group Name parameter (Example: The Anh)',
#             type=openapi.TYPE_STRING
#         )
#     ]
# )