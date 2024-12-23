from rest_framework.pagination import  PageNumberPagination


class MyPageSize(PageNumberPagination):
    page_size = 5