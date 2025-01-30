from django.db.models import Count
from django.db.models.functions import TruncYear, TruncMonth, TruncQuarter
from .models import User, Account, Post

# Thống kê số lượng người dùng
def load_users(params={}):
    query = User.objects.all()

    keyword = params.get("username") #Tích hợp username
    if keyword:
        query = query.filter(username__icontains=keyword)

    return query



# Thống kê số lượng bài viết
def load_posts(params={}):
    query = Post.objects.all()

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(post_content__icontains=keyword)

    return query

# Đếm số bài viết theo từng tài khoản (Top 5 người đăng nhiều nhất)
def count_posts_by_account(params={}):
    query = Account.objects.annotate(count=Count('post__id')).values(
        'id', 'phone_number', 'user__username',
        'user__first_name', 'user__last_name', 'count'
    ).order_by('-count')

    start_date = params.get('start_date')
    end_date = params.get('end_date')

    if start_date and end_date:
        query = query.filter(post__created_date__range=(start_date, end_date))
    elif start_date:
        query = query.filter(post__created_date__gte=start_date)
    elif end_date:
        query = query.filter(post__created_date__lte=end_date)

    return query[:5]  # Lấy 5 tài khoản có số bài viết nhiều nhất

# Đếm số bài viết theo năm, tháng hoặc quý
def count_posts_by_time_unit(params={}):
    time_unit = params.get('time_unit', 'year')  # Mặc định là theo năm
    start_date = params.get('start_date')
    end_date = params.get('end_date')

    if time_unit == 'year':
        query = Post.objects.annotate(time_unit=TruncYear('created_date'))
    elif time_unit == 'month':
        query = Post.objects.annotate(time_unit=TruncMonth('created_date'))
    elif time_unit == 'quarter':
        query = Post.objects.annotate(time_unit=TruncQuarter('created_date'))
    else:
        return []  # Nếu time_unit không hợp lệ

    query = query.values('time_unit') \
        .annotate(count=Count('id')) \
        .order_by('-time_unit')

    if start_date and end_date:
        query = query.filter(created_date__range=(start_date, end_date))
    elif start_date:
        query = query.filter(created_date__gte=start_date)
    elif end_date:
        query = query.filter(created_date__lte=end_date)

    # Chuyển đổi time_unit thành chuỗi cho JSON
    return [
        {'time_unit': item['time_unit'].strftime('%Y-%m-%d'), 'count': item['count']}
        for item in query
    ]
