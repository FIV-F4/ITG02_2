# module_analytics/views.py

from decimal import Decimal
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from module_orders.models import Order
from .models import Report, AggregateReport
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta


@staff_member_required
def report_list(request):
    """
    Представление для отображения списка индивидуальных отчетов.

    1. Ищет заказы без отчета.
    2. Создает отчеты для новых заказов.
    3. Отображает список отчетов.
    """
    # Найти заказы, которые не включены в отчеты
    orders_without_report = Order.objects.exclude(
        id__in=Report.objects.values_list('order_id', flat=True)
    )

    # Создать отчеты для новых заказов
    for order in orders_without_report:
        total_sales = sum(
            op.quantity * op.price for op in order.orderproduct_set.all()
        )
        expenses = total_sales * Decimal('0.7')  # Пример: 70% от продаж идут на расходы
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


@staff_member_required
def aggregate_report(request, period='daily'):
    """
    Генерирует агрегированный отчёт за указанный период.

    Параметры:
    - period: 'daily', 'weekly' или 'monthly'.
    """
    today = timezone.now().date()
    if period == 'daily':
        start_date = today - timedelta(days=1)
    elif period == 'weekly':
        start_date = today - timedelta(days=7)
    elif period == 'monthly':
        start_date = today - timedelta(days=30)
    else:
        # Если период не распознан, по умолчанию берем ежедневный
        start_date = today - timedelta(days=1)

    end_date = today

    # Фильтруем заказы за указанный период
    orders = Order.objects.filter(date__range=(start_date, end_date))

    # Вычисляем общую сумму продаж
    total_sales = orders.annotate(
        order_total=Sum(F('orderproduct__quantity') * F('orderproduct__price'))
    ).aggregate(total_sales=Sum('order_total'))['total_sales'] or 0

    total_expenses = total_sales * Decimal('0.7')
    total_profit = total_sales - total_expenses
    total_orders = orders.count()
    total_products_sold = orders.aggregate(
        total=Sum('orderproduct__quantity')
    )['total'] or 0

    # Создаем или обновляем отчёт
    report, created = AggregateReport.objects.update_or_create(
        period_type=period,
        start_date=start_date,
        end_date=end_date,
        defaults={
            'total_sales': total_sales,
            'total_profit': total_profit,
            'total_expenses': total_expenses,
            'total_orders': total_orders,
            'total_products_sold': total_products_sold,
        }
    )

    return render(request, 'module_analytics/aggregate_report.html', {'report': report})
