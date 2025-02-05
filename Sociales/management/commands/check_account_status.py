from django.core.management.base import BaseCommand
from Sociales.models import Account

class Command(BaseCommand):
    help = 'Kiểm tra và khóa tài khoản nếu không đổi mật khẩu sau 12 giờ'

    def handle(self, *args, **kwargs):
        accounts = Account.objects.filter(account_status=True)
        for account in accounts:
            account.check_and_update_status()
        self.stdout.write("Đã kiểm tra trạng thái tất cả các tài khoản.")
