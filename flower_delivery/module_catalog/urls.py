from django.urls import path
from . import views  # Импортируем views целиком

urlpatterns = [
    path('', views.catalog, name='catalog'),
]