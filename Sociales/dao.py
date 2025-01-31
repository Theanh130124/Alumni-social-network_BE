from django.db.models import Count
from django.db.models.functions import TruncYear, TruncMonth, TruncQuarter
from django.utils import timezone
from .models import *


def count_users_by_time_unit(time_unit='year'):
    """
    Đếm số lượng người dùng theo năm, tháng hoặc quý.
    """
    if time_unit == 'year':
        query = User.objects.annotate(time_unit=TruncYear('date_joined'))
    elif time_unit == 'month':
        query = User.objects.annotate(time_unit=TruncMonth('date_joined'))
    elif time_unit == 'quarter':
        query = User.objects.annotate(time_unit=TruncQuarter('date_joined'))
    else:
        return []

    query = query.values('time_unit') \
        .annotate(count=Count('id')) \
        .order_by('time_unit')

    return [
        {'time_unit': item['time_unit'].strftime('%Y-%m-%d'), 'count': item['count']}
        for item in query
    ]

def count_posts_by_time_unit(time_unit='year'):
    """
    Đếm số lượng bài viết theo năm, tháng hoặc quý.
    """
    if time_unit == 'year':
        query = Post.objects.annotate(time_unit=TruncYear('created_date'))
    elif time_unit == 'month':
        query = Post.objects.annotate(time_unit=TruncMonth('created_date'))
    elif time_unit == 'quarter':
        query = Post.objects.annotate(time_unit=TruncQuarter('created_date'))
    else:
        return []

    query = query.values('time_unit') \
        .annotate(count=Count('id')) \
        .order_by('time_unit')

    return [
        {'time_unit': item['time_unit'].strftime('%Y-%m-%d'), 'count': item['count']}
        for item in query
    ]
