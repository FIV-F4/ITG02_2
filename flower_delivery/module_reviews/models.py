# module_reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from module_catalog.models import Products

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])  # Рейтинг от 1 до 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    class Meta:
        ordering = ['-created_at']  # Последние отзывы будут показываться первыми
