"""
Путь: module_reg_auth_user/admin.py
Админ-панель для управления пользователями.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Кастомная админ-панель для модели пользователя с дополнительными полями.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'address', 'name', 'telegram_id')}),
    )
    list_display = ('username', 'email', 'phone', 'address', 'name', 'telegram_id', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone', 'address', 'name', 'telegram_id')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
