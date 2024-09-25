# Generated by Django 5.1 on 2024-09-25 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_analytics', '0003_aggregatereport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggregatereport',
            name='total_expenses',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='aggregatereport',
            name='total_orders',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='aggregatereport',
            name='total_products_sold',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='aggregatereport',
            name='total_profit',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='aggregatereport',
            name='total_sales',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
