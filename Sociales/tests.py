# from rest_framework.test import APIClient
# from django.test import TestCase
# from django.contrib.auth.models import User
#
# class UserCreateTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_create_user(self):
#         url = '/users/'  # URL cho endpoint tạo người dùng
#         data = {
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'email': 'john.doe@example.com',
#             'password': 'password123'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 201)  # Kiểm tra mã phản hồi là 201 (tạo thành công)
#         user = User.objects.get(email='john.doe@example.com')  # Kiểm tra người dùng đã được tạo chưa
#         self.assertTrue(user.check_password('password123'))  # Kiểm tra mật khẩu đã được mã hóa đúng chưa
#
# class UserUpdateTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             first_name='Jane',
#             last_name='Doe',
#             email='jane.doe@example.com',
#             password='oldpassword123'
#         )
#
#     def test_update_user(self):
#         url = f'/users/{self.user.id}/'  # URL cho endpoint cập nhật người dùng
#         data = {
#             'first_name': 'Jane',
#             'last_name': 'Smith',
#             'email': 'jane.smith@example.com',
#             'password': 'newpassword123'
#         }
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, 200)  # Kiểm tra mã phản hồi là 200 (cập nhật thành công)
#         self.user.refresh_from_db()  # Lấy lại người dùng sau khi cập nhật
#         self.assertEqual(self.user.first_name, 'Jane')
#         self.assertEqual(self.user.last_name, 'Smith')
#         self.assertEqual(self.user.email, 'jane.smith@example.com')
#         self.assertTrue(self.user.check_password('newpassword123'))  # Kiểm tra mật khẩu mới đã được mã hóa đúng chưa
