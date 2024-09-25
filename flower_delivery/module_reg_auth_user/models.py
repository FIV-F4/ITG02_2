"""
Путь: module_reg_auth_user/models.py
Модели для управления пользователями.
"""

from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями.
    """
    groups = models.ManyToManyField(
        Group, related_name='custom_user_set', blank=True,
        help_text='The groups this user belongs to.', verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions_set', blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, help_text='Телефонный номер пользователя'
    )
    address = models.TextField(
        blank=True, null=True, help_text='Адрес пользователя'
    )
    email = models.EmailField(
        unique=True, help_text='Электронная почта пользователя'
    )
    name = models.CharField(
        max_length=255, blank=True, null=True, help_text='Имя пользователя'
    )
    telegram_id = models.CharField(
        max_length=50, blank=True, null=True, help_text='Telegram ID пользователя'
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Метаданные модели, включая пользовательские разрешения.
        """
        permissions = [
            ("view_profile", "Can view profile"),
            ("edit_profile", "Can edit profile")
        ]

    def __str__(self):
        return str(self.username)
