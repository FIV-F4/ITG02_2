"""
Путь: module_analytics/migrations/0002_initial.py
Автоматически сгенерированная миграция для добавления связи Report и Order.
"""

# pylint: disable=C0301, C0103
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Миграция для добавления связи OneToOne между Report и Order.
    """

    initial = True

    dependencies = [
        ('module_analytics', '0001_initial'),
        ('module_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='module_orders.order'),
        ),
    ]
