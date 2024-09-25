"""
Путь: module_orders/migrations/0001_initial.py
Автоматически сгенерированная миграция для создания моделей.
"""

# pylint: disable=C0103, C0301
from django.db import migrations, models

class Migration(migrations.Migration):
    """
    Миграция для создания моделей Order, OrderProduct и Delivery.
    """
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[
                    ('cart', 'Корзина'), ('ordered', 'Оформлен'), ('shipped', 'Отправлен'),
                    ('delivered', 'Доставлен'), ('cancelled', 'Отменен')
                ], max_length=50, default='cart')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
