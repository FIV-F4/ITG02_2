"""
Путь: module_catalog/tests.py
Тесты для приложения module_catalog.
"""
from django.test import TestCase
from module_catalog.models import Products

class ProductsModelTest(TestCase):
    def setUp(self):
        self.product = Products.objects.create(
            name='Роза',
            price=50.00,
            image='images/products/rose.jpg'
        )

    def test_product_creation(self):
        """Проверка создания продукта и его представления"""
        self.assertEqual(self.product.name, 'Роза')
        self.assertEqual(self.product.price, 50.00)
        self.assertEqual(self.product.image, 'images/products/rose.jpg')
        self.assertEqual(str(self.product), 'Роза')
