"""
Путь: module_orders/models.py
Модели для управления заказами, продуктами и доставкой.
"""

from django.db import models
from django.conf import settings

class Order(models.Model):
    """
    Модель заказа.
    """
    STATUS_CHOICES = [
        ('cart', 'Корзина'),
        ('ordered', 'Оформлен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='cart')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"  # Строковое представление продукта в заказе  # pylint: disable=no-member

    def is_ordered(self):
        """
        Проверяет, был ли заказ оформлен.
        Возвращает True, если заказ имеет статус 'ordered'.
        """
        return self.status == 'ordered'

class OrderProduct(models.Model):
    """
    Модель продукта в заказе.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('module_catalog.Products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.product.name} в заказе {self.order.id}"

class Delivery(models.Model):
    """
    Модель доставки для заказа.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Доставка для заказа {self.order.id} на адрес {self.address}"

# Подавление предупреждения для примера кода
# pylint: disable=pointless-string-statement
'''
@receiver(post_save, sender=Order)
def send_status_update(sender, instance, **kwargs):
    """
    Отправляет уведомление о изменении статуса заказа.
    """
    from module_telegram.bot import notify_status_change
    if instance.status != 'cart':
        import asyncio
        asyncio.run(notify_status_change(instance.id))
'''
