from django.core.mail import send_mail
from pyexpat.errors import messages


#Gui mail cho giang vien de doi pass

#Xu ly them duong dan toi cho doi password luon (chưa làm)
def send_account_creation_email(user,password):
    subject = "Thông tin tài khoản"
    messages = (f'Chào {user.first_name},\n\nTài Khoản của bạn đã được tạo thành công.\n\n'
                f'Tên đăng nhập:{user.username}\nMật khẩu mặc đinh:  ou@123\n\nLưu ý:' #Để user.password nó bị băm
                f'Bạn cần thay đổi mật khẩu trong vòng 24 giờ , <nữa để đường dẫn trỏ tới thay đổi pass>')
    send_mail(subject,messages,'theanhtran130124@gmail.com',[user.email])

def send_mail_for_post_invited(post_invitation, emails):
    subject = f"Lời mời tham gia sự kiện: {post_invitation.event_name}"
    message = (
        f"Bạn được mời tham gia sự kiện: {post_invitation.event_name}\n"
        f"Thời gian bắt đầu: {post_invitation.start_time}\n"
        f"Thời gian kết thúc: {post_invitation.end_time}\n"
        f"Để biết thêm thông tin, vui lòng truy cập liên kết sự kiện."
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='theanhtran130124@gmail.com',
            recipient_list=list(emails),
            fail_silently=False,
        )
    except Exception as e:
        raise Exception(f"Lỗi khi gửi email: {str(e)}")

