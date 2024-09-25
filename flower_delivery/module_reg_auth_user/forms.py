"""
Путь: module_reg_auth_user/forms.py
Формы для управления регистрацией и Telegram ID.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):  # pylint: disable=too-many-ancestors
    """
    Кастомная форма регистрации пользователя.
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Мета-класс для указания модели и полей формы.
        """
        model = User
        fields = ['username', 'email', 'phone', 'address', 'name']

class TelegramIDForm(forms.ModelForm):  # pylint: disable=too-few-public-methods
    """
    Форма для ввода и редактирования Telegram ID пользователя.
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Мета-класс для указания модели и полей формы.
        """
        model = User
        fields = ['telegram_id']
        labels = {'telegram_id': 'Ваш Telegram ID'}
