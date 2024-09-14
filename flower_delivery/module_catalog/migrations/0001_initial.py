"""
Путь: module_catalog/migrations/0001_initial.py
Автоматически сгенерированная миграция для создания модели Products.
"""

# pylint: disable=C0301, C0103
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Миграция для создания модели Products.
    """

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='images/products')),
            ],
        ),
    ]
