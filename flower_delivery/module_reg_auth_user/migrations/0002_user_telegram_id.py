# Generated by Django 5.1 on 2024-09-08 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_reg_auth_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(blank=True, help_text='Telegram ID пользователя', max_length=50, null=True),
        ),
    ]
