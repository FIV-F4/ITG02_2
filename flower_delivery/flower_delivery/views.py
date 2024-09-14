"""
Путь: flower_delivery/views.py
Представления для приложения flower_delivery.
"""

from django.shortcuts import render

def index(request):
    """
    Представление для главной страницы.
    Отображает страницу 'index.html'.
    """
    return render(request, 'index.html')
