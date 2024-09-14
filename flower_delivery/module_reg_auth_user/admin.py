from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Добавляем поля в fieldsets для отображения на странице редактирования пользователя
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'address', 'name', 'telegram_id')}),
    )

    # Добавляем поля в list_display для отображения в общем списке пользователей
    list_display = ('username', 'email', 'phone', 'address', 'name', 'telegram_id')

    # Добавляем возможность поиска по полям
    search_fields = ('username', 'email', 'phone', 'address', 'name', 'telegram_id')

    # Добавляем сортировку по полям
    ordering = ('username',)

    # Добавляем поля в list_filter для фильтрации
    list_filter = ('is_staff', 'is_superuser', 'is_active')
