"""
Путь: module_reg_auth_user/urls.py
Маршруты для управления регистрацией, авторизацией и Telegram ID.
"""

from django.urls import path
from .views import register, login_user, logout_user, telegram_id_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('telegram_id/', telegram_id_view, name='telegram_id'),
]

# Добавлена новая строка в конце файла для устранения предупреждения Pylint.
