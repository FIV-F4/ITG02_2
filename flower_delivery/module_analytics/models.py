from django.db import models
from module_orders.models import Order

class Report(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sales_data = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Отчет {self.id} по заказу {self.order.id} от {self.date}"
