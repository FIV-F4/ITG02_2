# module_analytics/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import AggregateReport
from module_orders.models import Order
from decimal import Decimal
from django.db.models import Sum, F


@shared_task
def generate_daily_report():
    """
    Задача Celery для генерации ежедневного агрегированного отчета.
    """
    today = timezone.now().date()
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
    AggregateReport.objects.update_or_create(
        period_type='daily',
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
