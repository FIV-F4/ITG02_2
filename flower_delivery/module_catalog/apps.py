"""
Путь: module_catalog/apps.py
Конфигурация приложения module_catalog.
"""

from django.apps import AppConfig

class ModuleCatalogConfig(AppConfig):
    """
    Конфигурационный класс для приложения module_catalog.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_catalog'
