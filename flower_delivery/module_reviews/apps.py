"""
Путь: module_reviews/apps.py
Конфигурация приложения для отзывов.
"""

from django.apps import AppConfig

class ModuleReviewsConfig(AppConfig):
    """
    Конфигурационный класс для приложения отзывов.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_reviews'
