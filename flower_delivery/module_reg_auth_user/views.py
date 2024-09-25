"""
Путь: module_reg_auth_user/views.py
Представления для управления регистрацией, авторизацией и Telegram ID.
"""

import base64
from io import BytesIO
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import qrcode
from .forms import CustomUserCreationForm, TelegramIDForm

def register(request):
    """
    Обрабатывает регистрацию нового пользователя.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('home')
    form = CustomUserCreationForm()
    return render(request, 'module_reg_auth_user/register.html', {'form': form})

def login_user(request):
    """
    Обрабатывает вход пользователя в систему.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('home')
        messages.error(request, 'Неверное имя пользователя или пароль.')
    form = AuthenticationForm()
    return render(request, 'module_reg_auth_user/login.html', {'form': form})

def logout_user(request):
    """
    Обрабатывает выход пользователя из системы.
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('home')

@login_required
def telegram_id_view(request):
    """
    Управление Telegram ID и генерация QR-кода для Telegram бота.
    """
    if request.method == 'POST':
        form = TelegramIDForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('telegram_id')
    form = TelegramIDForm(instance=request.user)

    # Генерация QR-кода
    telegram_bot_link = 'https://t.me/FIV_TG01_bot'
    qr = qrcode.make(telegram_bot_link)

    # Сохраняем изображение в байтовый поток
    qr_io = BytesIO()
    qr.save(qr_io, format="PNG")
    qr_io.seek(0)

    # Преобразуем изображение в строку Base64
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode('utf-8')

    context = {
        'form': form,
        'telegram_bot_link': telegram_bot_link,
        'qr_code_base64': qr_base64
    }
    return render(request, 'module_reg_auth_user/telegram_id.html', context)
