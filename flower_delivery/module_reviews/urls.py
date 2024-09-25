"""
Путь: module_reviews/urls.py
Маршруты для управления отзывами на продукты.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
]
