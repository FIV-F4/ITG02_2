# flower_delivery/flower_delivery/celery_app.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Устанавливаем модуль настроек Django для приложения Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')

app = Celery('flower_delivery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
