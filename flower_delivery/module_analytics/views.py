# module_analytics/views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from module_orders.models import Order
from decimal import Decimal

@staff_member_required
def report_list(request):
    # Найти заказы, которые не включены в отчеты
    orders_without_report = Order.objects.exclude(id__in=Report.objects.values_list('order_id', flat=True))

    # Создать отчеты для новых заказов
    for order in orders_without_report:
        # Пример расчета прибыли, расходов и данных по продажам
        # Это можно изменить в зависимости от вашей логики
        total_sales = sum([op.quantity * op.price for op in order.orderproduct_set.all()])
        expenses = total_sales * Decimal('0.7')  # Пример: 70% от продаж идут на расходы
 # Пример: 70% от продаж идут на расходы
        profit = total_sales - expenses

        # Создать отчет
        Report.objects.create(
            order=order,
            sales_data=total_sales,
            profit=profit,
            expenses=expenses
        )

    # Отобразить список всех отчетов
    reports = Report.objects.all().order_by('-date')
    return render(request, 'module_analytics/report_list.html', {'reports': reports})
