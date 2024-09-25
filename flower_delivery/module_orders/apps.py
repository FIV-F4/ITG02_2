"""
Путь: module_orders/apps.py
Конфигурация приложения module_orders.
"""

from django.apps import AppConfig

class ModuleOrdersConfig(AppConfig):
    """
    Конфигурационный класс для приложения module_orders.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_orders'

    def ready(self):
        """
        Инициализация модуля приложения.
        """
        import module_orders.signals  # Регистрация сигналов