"""
Путь: module_analytics/views.py
Представления для приложения module_analytics.
"""

from decimal import Decimal
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from module_orders.models import Order
from .models import Report

@staff_member_required
def report_list(request):
    """
    Представление для отображения списка отчетов.

    1. Ищет заказы без отчета.
    2. Создает отчеты для новых заказов.
    3. Отображает список отчетов.
    """
    # Найти заказы, которые не включены в отчеты
    orders_without_report = Order.objects.exclude(  # pylint: disable=no-member
        id__in=Report.objects.values_list('order_id', flat=True)  # pylint: disable=no-member
    )

    # Создать отчеты для новых заказов
    for order in orders_without_report:
        total_sales = sum(
            op.quantity * op.price for op in order.orderproduct_set.all()
        )  # Используем генератор для оптимизации
        expenses = total_sales * Decimal('0.7')  # Пример: 70% от продаж идут на расходы
        profit = total_sales - expenses

        # Создать отчет
        Report.objects.create(  # pylint: disable=no-member
            order=order,
            sales_data=total_sales,
            profit=profit,
            expenses=expenses
        )

    # Отобразить список всех отчетов
    reports = Report.objects.all().order_by('-date')  # pylint: disable=no-member
    return render(request, 'module_analytics/report_list.html', {'reports': reports})
