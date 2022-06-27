from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseTestCase(TestCase):

    def setUp(self) -> None:
        self.register_url = reverse('signup')
        self.login_url = reverse('login')

        self.user = {
            "email": "test1@gmail.com", 
            "username": "test1",
            "password": "password", 
            }

        self.user_short_pass = {
            "email": "test2@gmail.com", 
            "username": "test2",
            "password": "pass"
            }

        self.user_no_password = {
            'username': 'username', 
            'password': ''
            }

        self.user_no_username =  {
            'username': '',
            'password': 'password'
            }

class RegisterTestCase(BaseTestCase):

    def test_can_register_user(self):
        response = self.client.post(self.register_url, data=self.user)
        self.assertEqual(response.status_code, 201)
    
    def test_cant_register_with_shortpass(self):
        response = self.client.post(self.register_url, self.user_short_pass)
        self.assertEqual(response.status_code, 400)


class LoginTest(BaseTestCase):

    def test_login_success(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, 200)

    def test_cant_login_with_no_username(self):
        response = self.client.post(self.login_url, self.user_no_username)
        self.assertEqual(response.status_code, 400)

    def test_cant_login_with_no_password(self):
        response= self.client.post(self.login_url, self.user_no_password)
        self.assertEqual(response.status_code, 400)