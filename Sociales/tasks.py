from datetime import timezone
from venv import logger
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from models import *
from .serializers import InvitationGroup
from rest_framework.renderers import JSONRenderer
@shared_task(blind=True)
def change_password_after_1_days():
    try:
        time_deadline = timezone.now() - timedelta(days=1)
        lecturers = User.objects.filter(
            account__role = UserRole.LECTURER,
            password_changed_at__isnull= True, #Chưa đổi pass lần nào thì nó là null
            date_joined__lte=time_deadline #Thời gian tạo <= Thời gian đổi pass + 24h -> những ng đã chưa đổi pass quá 24h
        )
        for lecturer in lecturers:
            account = lecturer.account
            account.account_status = False #Khóa trạng thái đăng nhập
            account.save()
        logger.info("Task (change_password_after_1_days) đã thực hiện thành công")
        print("Task (change_password_after_1_days) đã thực hiện thành công ")
        return "Task (change_password_after_1_days) Competed"
    except Exception as e:
        logger.error("Task (change_password_after_1_days) thất bại: %s", str(e))
        return 'Task (change_password_after_1_days) Failed'

