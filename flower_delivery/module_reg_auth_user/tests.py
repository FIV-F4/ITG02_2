"""
Путь: module_reg_auth_user/tests.py
Тесты для приложения управления пользователями.
"""

from django.test import TestCase
from module_reg_auth_user.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='testuser@example.com',
            phone='1234567890',
            address='Улица Пушкина, дом Колотушкина',
            name='Иван Иванович',
            telegram_id='123456'
        )

    def test_user_creation(self):
        """Проверка создания пользователя и его данных"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.address, 'Улица Пушкина, дом Колотушкина')
        self.assertEqual(self.user.name, 'Иван Иванович')
        self.assertEqual(self.user.telegram_id, '123456')
        self.assertEqual(str(self.user), 'testuser')

    def test_user_permissions(self):
        """Проверка наличия пользовательских разрешений"""
        permission = self.user.user_permissions.create(
            codename='view_profile',
            name='Can view profile',
            content_type_id=1  # Возможно, потребуется указать корректный content_type_id
        )
        self.assertTrue(self.user.user_permissions.filter(codename='view_profile').exists())

    def test_user_groups(self):
        """Проверка наличия групп у пользователя"""
        group = self.user.groups.create(name='Test Group')
        self.user.groups.add(group)
        self.assertTrue(self.user.groups.filter(name='Test Group').exists())
