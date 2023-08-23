from django.db import models
from django.contrib.auth.models import AbstractUser


def get_image_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.username, filename)


class User(AbstractUser):
    """Модель пользователя"""
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'





