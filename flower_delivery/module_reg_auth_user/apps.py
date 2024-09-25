"""
Путь: module_reg_auth_user/apps.py
Конфигурация приложения для управления пользователями.
"""

from django.apps import AppConfig

class ModuleRegAuthUserConfig(AppConfig):
    """
    Конфигурационный класс для приложения регистрации и аутентификации пользователей.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_reg_auth_user'
