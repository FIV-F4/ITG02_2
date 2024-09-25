"""
Путь: module_telegram/apps.py
Конфигурация приложения для модуля Telegram.
"""

from django.apps import AppConfig

class ModuleTelegramConfig(AppConfig):
    """
    Конфигурационный класс для приложения Telegram.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_telegram'
