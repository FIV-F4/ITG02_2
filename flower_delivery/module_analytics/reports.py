# module_analytics/reports.py

from module_orders.models import Order, OrderProduct
from django.db.models import Sum, Count, Avg, F, DecimalField
from django.db.models.functions import TruncDay
from datetime import datetime

def generate_detailed_report():
    """
    Генерирует подробный отчёт по заказам и продажам.
    """
    total_orders = Order.objects.count()

    # Вычисляем общую выручку, суммируя стоимость каждого OrderProduct
    total_revenue = OrderProduct.objects.aggregate(
        total=Sum(F('quantity') * F('price'), output_field=DecimalField())
    )['total'] or 0

    # Вычисляем средний чек
    average_order_value = OrderProduct.objects.values('order').annotate(
        order_total=Sum(F('quantity') * F('price'))
    ).aggregate(avg=Avg('order_total'))['avg'] or 0

    # Продажи по дням
    sales_by_day = OrderProduct.objects.annotate(
        day=TruncDay('order__date')
    ).values('day').annotate(
        total_sales=Sum(F('quantity') * F('price'), output_field=DecimalField()),
        orders=Count('order', distinct=True)
    ).order_by('day')

    report = f"📊 *Подробный отчёт по заказам:*\n\n"
    report += f"• Всего заказов: *{total_orders}*\n"
    report += f"• Общая выручка: *{total_revenue:.2f} руб.*\n"
    report += f"• Средний чек: *{average_order_value:.2f} руб.*\n\n"
    report += "*Продажи по дням:*\n"

    for entry in sales_by_day:
        day = entry['day'].strftime('%d-%m-%Y')
        total_sales = entry['total_sales'] or 0
        orders_count = entry['orders']
        report += f"📅 {day} — Заказов: *{orders_count}*, Выручка: *{total_sales:.2f} руб.*\n"

    return report
