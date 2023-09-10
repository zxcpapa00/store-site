from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


def get_image_path(instance, filename):
    """Функция создания динамического url для изображений пользователей"""
    return 'users/{0}/{1}'.format(instance.username, filename)


class User(AbstractUser):
    """Модель пользователя"""
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    email = models.EmailField(blank=True)
    is_verification = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    """Модель письма для верификации"""
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verify', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        message = 'Для подтверждения учётной записи для {0} перейдите по ссылке {1}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
