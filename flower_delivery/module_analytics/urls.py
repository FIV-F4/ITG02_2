"""
Путь: module_analytics/urls.py
Маршруты для приложения module_analytics.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_list, name='report_list'),
]
