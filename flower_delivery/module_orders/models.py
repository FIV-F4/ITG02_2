# module_orders/models.py

from django.db import models
from django.conf import settings

# Модель для хранения информации о заказе
class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Корзина'),       # Заказ еще в корзине, не оформлен
        ('ordered', 'Оформлен'),   # Заказ подтвержден пользователем
        ('shipped', 'Отправлен'),  # Заказ отправлен покупателю
        ('delivered', 'Доставлен'),# Заказ доставлен
        ('cancelled', 'Отменен'),  # Заказ отменен
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='cart')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление объекта заказа.
        """
        return f"Order {self.id} - {self.get_status_display()}"

    def is_ordered(self):
        """
        Проверяет, был ли заказ оформлен.
        """
        return self.status == 'ordered'

# Модель для хранения информации о товарах в заказе
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('module_catalog.Products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Модель для хранения информации о доставке
class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)


# Код для отправки обновлений о статусе заказа
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
