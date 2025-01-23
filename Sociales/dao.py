from itertools import count

from django.db.models import  Count
from oauthlib.uri_validate import query

from .models import *

#Thong ke so nguoi dung

def load_users(params={}):
    query = User.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(username__icontains=keyword)

    return query

def load_account(params={}):
    query = Account.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(phone_number__icontains=keyword)

    role = params.get("role")
    if role:
        query = query.filter(role=role)


    group_account_id = params.get("group_account_id")
    if group_account_id:
        query = query.filter(group_account_id=group_account_id)

    return query

def load_posts(params={}):
    query = Post.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(post_content__icontains=keyword)

    return query

#Dem bai viet account

def count_posts_by_account(params={}):
    query = Account.objects.annotate(count=Count('post_id')).values('id', 'phone_number', 'user__username',
                                                                     'user__first_name', 'user__last_name',
                                                                     'count').order_by('-count')
    start_date = params.get('start_date')
    end_date = params.get('end_date')

    if start_date and end_date:
        query = query.filter(post__created_date__range=(start_date, end_date))
    elif start_date:
        query = query.filter(post__created_date__gte=start_date)
    elif end_date:
        query = query.filter(post__created_date__lte=end_date)

    return query[:5] #-> lấy 5 bài thôi


from django.db.models import Count
from django.db.models.functions import TruncYear , TruncMonth , TruncQuarter

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear, TruncQuarter


def count_posts_by_time_unit(params={}):
    time_unit = params.get('time_unit', 'year')  # Thời gian mặc định là theo năm
    start_date = params.get('start_date')
    end_date = params.get('end_date')

    if time_unit == 'year':
        query = Post.objects.annotate(time_unit=TruncYear('created_date'))
    elif time_unit == 'month':
        query = Post.objects.annotate(time_unit=TruncMonth('created_date'))
    elif time_unit == 'quarter':
        query = Post.objects.annotate(time_unit=TruncQuarter('created_date'))

    query = query.values('time_unit') \
        .annotate(count=Count('id')) \
        .order_by('-time_unit')

    if start_date and end_date:
        query = query.filter(created_date__range=(start_date, end_date))
    elif start_date:
        query = query.filter(created_date__gte=start_date)
    elif end_date:
        query = query.filter(created_date__lte=end_date)

    return query
