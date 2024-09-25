# module_analytics/models.py

from django.db import models
from module_orders.models import Order


class Report(models.Model):
    """
    Модель отчета, связанная с конкретным заказом.

    Поля:
    - order: Связь один к одному с моделью Order.
    - date: Дата создания отчета.
    - sales_data: Данные о продажах.
    - profit: Прибыль.
    - expenses: Расходы.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sales_data = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Отчет {self.id} по заказу {self.order.id} от {self.date}"


class AggregateReport(models.Model):
    """
    Модель агрегированного отчета за определенный период.

    Поля:
    - period_type: daily, weekly, monthly.
    - start_date: Начальная дата периода.
    - end_date: Конечная дата периода.
    - total_sales: Общая сумма продаж.
    - total_profit: Общая прибыль.
    - total_expenses: Общие расходы.
    - total_orders: Общее количество заказов.
    - total_products_sold: Общее количество проданных товаров.
    """
    PERIOD_CHOICES = [
        ('daily', 'Ежедневный'),
        ('weekly', 'Еженедельный'),
        ('monthly', 'Ежемесячный'),
    ]

    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    total_products_sold = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_period_type_display()} отчет с {self.start_date} по {self.end_date}"
