# Generated by Django 5.1 on 2024-09-25 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module_reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at', 'id']},
        ),
    ]
