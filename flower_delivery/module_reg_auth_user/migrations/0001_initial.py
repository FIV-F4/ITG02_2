"""
Путь: module_reg_auth_user/migrations/0001_initial.py
Миграция для создания модели пользователя.
"""

# pylint: disable=C0301,C0103
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    """
    Миграция для создания модели пользователя.
    """
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('telegram_id', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('view_profile', 'Can view profile'), ('edit_profile', 'Can edit profile')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
