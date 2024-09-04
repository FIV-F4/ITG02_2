from django.db import models

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Корзина'),  # Заказ еще в корзине, не оформлен
        ('ordered', 'Оформлен'),  # Заказ подтвержден пользователем
        ('shipped', 'Отправлен'),  # Заказ отправлен покупателю
        ('delivered', 'Доставлен'),  # Заказ доставлен
        ('cancelled', 'Отменен'),  # Заказ отменен
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='cart')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"

    def is_ordered(self):
        return self.status == 'ordered'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('module_catalog.Products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)
