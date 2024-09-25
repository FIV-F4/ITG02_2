"""
Путь: module_reviews/forms.py
Формы для управления отзывами.
"""

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):  # pylint: disable=too-few-public-methods
    """
    Форма для отправки отзыва.
    """
    class Meta:  # pylint: disable=too-few-public-methods
        """
        Мета-класс для формы отзыва.
        """
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
