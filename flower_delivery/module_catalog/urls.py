"""
Путь: module_catalog/urls.py
Маршруты для приложения module_catalog.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
]

# Добавлена новая строка в конце файла для устранения предупреждения.
