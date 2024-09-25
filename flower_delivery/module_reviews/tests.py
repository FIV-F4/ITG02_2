# module_reviews/tests.py

from django.test import TestCase
from module_reviews.models import Review
from module_catalog.models import Products
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Products.objects.create(
            name='Роза',
            price=50.00,
            image='images/products/rose.jpg'
        )

        # Создаем первый отзыв с точным указанием времени создания
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Очень хороший продукт!',
            created_at=timezone.now() - timedelta(days=1, seconds=10)  # Вчерашний день, чуть раньше
        )

    def test_review_creation(self):
        """Проверка создания отзыва и корректного представления"""
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Очень хороший продукт!')
        self.assertEqual(
            str(self.review),
            f"Отзыв от {self.review.user.username} на {self.review.product.name}"
        )

    def test_review_ordering(self):
        """
        Проверка сортировки отзывов по дате создания.
        """
        # Создаём второй отзыв с более поздней датой
        another_review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Ещё один отличный продукт."
        )

        # Получаем все отзывы
        reviews = list(Review.objects.all())

        # Проверяем, что более поздний отзыв находится первым
        self.assertEqual(reviews[0], another_review)

    def test_review_ordering_with_same_timestamp(self):
        """
        Проверка сортировки отзывов с одинаковыми временными метками.
        """
        # Создаём второй отзыв с той же датой
        another_review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Ещё один отличный продукт.",
            created_at=self.review.created_at  # Устанавливаем ту же дату создания
        )

        # Получаем все отзывы
        reviews = list(Review.objects.all())

        # Проверяем, что оригинальный отзыв (с меньшим id) находится первым
        self.assertEqual(reviews[0], self.review)
