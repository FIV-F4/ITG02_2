"""
Путь: module_reviews/models.py
Модели для отзывов.
"""

from django.db import models
from django.conf import settings
from module_catalog.models import Products

class Review(models.Model):
    """
    Модель отзыва о продукте.
    """
    product = models.ForeignKey(
        Products, related_name='reviews', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], default=1
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Метаданные модели.
        """
        ordering = ['-created_at', 'id']  # Сортировка по дате и по id в порядке возрастания

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"