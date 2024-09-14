# module_reg_auth_user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'name']

class TelegramIDForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['telegram_id']
        labels = {'telegram_id': 'Ваш Telegram ID'}