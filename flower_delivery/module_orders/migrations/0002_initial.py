"""
Путь: module_orders/migrations/0002_initial.py
Автоматически сгенерированная миграция для добавления связей между Order, OrderProduct и Delivery.
"""

# pylint: disable=C0103
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    """
    Миграция для добавления внешних ключей и связей между моделями.
    """

    initial = True

    dependencies = [
        ('module_catalog', '0001_initial'),
        ('module_orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='module_orders.order'
            ),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='module_orders.order'
            ),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='module_catalog.products'
            ),
        ),
    ]
