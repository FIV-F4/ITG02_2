# module_reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
]
