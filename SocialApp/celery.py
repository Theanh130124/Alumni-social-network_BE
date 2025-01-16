#Task Queue -> hàng đợi task -> xử lý tác vụ không đồng bộ hoặc định kỳ
import logging #Ghi lỗi vào log file
import os #làm việc file thư mục

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','SocialApp.settings')
app = Celery('SocialApp')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
@app.task(blind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    # 'run-create-invitation-group': {
    #     'task': '',
    #     'schedule': 30,  # Chạy task mỗi 30 giay
    # },
    'run-change-password-after-1-days': {
        'task': 'Sociales.tasks.change_password_after_1_days',
        'schedule': crontab(minute=0, hour=0),  # Chạy task mỗi ngày vào lúc 12h đêm
    },
    # 'test-count-task': {
    #     'task': 'Sociales.tasks.test_count_task',
    #     'schedule': 15
    # },
}

app.conf.broker_connection_retry_on_startup = True