"""
Путь: module_analytics/models.py
Модели для приложения module_analytics.
"""

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
        """
        Возвращает строковое представление отчета.
        """
        return f"Отчет {self.id} по заказу {self.order.id} от {self.date}"  # pylint: disable=no-member
