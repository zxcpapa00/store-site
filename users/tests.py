from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from users.forms import UserRegisterForm
from users.models import User


class UserRegistrationView(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post(self):
        data = {
            'first_name': 'Ivan', 'last_name': 'Dupin',
            'username': 'lolo11', 'email': 'pppg@mail.com',
            'password1': 'asdzxc123.', 'password2': 'asdzxc123.'
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        


