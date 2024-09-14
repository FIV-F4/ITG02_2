"""
Путь: flower_delivery/urls.py
Маршрутизация URL для приложения flower_delivery.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('catalog/', include('module_catalog.urls')),
    path('accounts/', include('module_reg_auth_user.urls')),
    path('orders/', include('module_orders.urls')),
    path('reviews/', include('module_reviews.urls')),
    path('analytics/', include('module_analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Добавлена новая строка для устранения предупреждения
