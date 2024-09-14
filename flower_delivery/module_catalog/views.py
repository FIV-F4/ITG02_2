"""
Путь: module_catalog/views.py
Представления для приложения module_catalog.
"""

from django.shortcuts import render
from .models import Products

def catalog(request):
    """
    Представление для отображения всех продуктов в каталоге.
    """
    products = Products.objects.all()  # pylint: disable=E1101
    return render(request, 'module_catalog/catalog.html', {'products': products})
