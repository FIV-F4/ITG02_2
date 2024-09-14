"""
Путь: module_analytics/migrations/0001_initial.py
Автоматически сгенерированная миграция для создания модели Report.
"""

# pylint: disable=C0301, C0103
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Миграция для создания модели Report.
    """

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sales_data', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expenses', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
