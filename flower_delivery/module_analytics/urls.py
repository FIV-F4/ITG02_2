# module_analytics/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_list, name='report_list'),
    path('aggregate_reports/<str:period>/', views.aggregate_report, name='aggregate_report'),
]
