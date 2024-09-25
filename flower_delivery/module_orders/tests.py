"""
Путь: module_orders/tests.py
Тесты для приложения module_orders.
"""
from django.test import TestCase
from module_orders.models import Order, OrderProduct, Delivery
from module_catalog.models import Products
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(user=self.user, status='ordered')

    def test_order_creation(self):
        """Проверка создания заказа и его представления"""
        self.assertEqual(self.order.status, 'ordered')
        self.assertEqual(str(self.order), f"Order {self.order.id} - Оформлен")

    def test_order_is_ordered(self):
        """Проверка метода is_ordered()"""
        self.assertTrue(self.order.is_ordered())

class OrderProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Products.objects.create(name='Роза', price=50.00, image='images/products/rose.jpg')
        self.order = Order.objects.create(user=self.user, status='ordered')
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=100.00
        )

    def test_order_product_creation(self):
        """Проверка создания продукта в заказе и его представления"""
        self.assertEqual(self.order_product.quantity, 2)
        self.assertEqual(self.order_product.price, 100.00)
        self.assertEqual(str(self.order_product), f"{self.order_product.product.name} в заказе {self.order_product.order.id}")

class DeliveryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(user=self.user, status='ordered')
        self.delivery = Delivery.objects.create(
            order=self.order,
            address='Улица Пушкина, дом Колотушкина',
            info='Доставить до 18:00'
        )

    def test_delivery_creation(self):
        """Проверка создания доставки и ее представления"""
        self.assertEqual(self.delivery.address, 'Улица Пушкина, дом Колотушкина')
        self.assertEqual(self.delivery.info, 'Доставить до 18:00')
        self.assertEqual(str(self.delivery), f"Доставка для заказа {self.delivery.order.id} на адрес {self.delivery.address}")

class OrderViewTest(TestCase):
    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Создаем продукт, который будет добавлен в корзину
        self.product = Products.objects.create(
            name='Роза',
            price=50.00,
            image='images/products/rose.jpg'
        )

        # Создаем заказ для пользователя
        self.order = Order.objects.create(user=self.user, status='cart')

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мои заказы')

    def test_add_to_cart_view(self):
        # Проверяем добавление товара в корзину
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Проверка, что происходит редирект после добавления товара в корзину