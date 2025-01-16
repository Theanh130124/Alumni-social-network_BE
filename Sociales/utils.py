from django.core.mail import send_mail
from pyexpat.errors import messages


#Gui mail cho giang vien de doi pass

#Xu ly them duong dan toi cho doi password luon (chưa làm)
def send_account_creation_email(user,password):
    subject = "Thông tin tài khoản"
    messages = (f'Chào {user.first_name},\n\nTài Khoản của bạn đã được tạo thành công.\n\n'
                f'Tên đăng nhập:{user.username}\nMật khẩu mặc đinh:  @ou123\n\nLưu ý:' #Để user.password nó bị băm
                f'Bạn cần thay đổi mật khẩu trong vòng 24 giờ , <nữa để đường dẫn trỏ tới thay đổi pass>')
    send_mail(subject,messages,'theanhtran130124@gmail.com',[user.email])