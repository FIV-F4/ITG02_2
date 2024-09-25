# module_analytics/admin.py

from django.contrib import admin
from .models import Report, AggregateReport

admin.site.register(Report)
admin.site.register(AggregateReport)
