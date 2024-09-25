"""
Путь: module_orders/forms.py
Формы для управления доставкой и заказами.
"""

from django import forms
from .models import Delivery

class DeliveryForm(forms.ModelForm): # pylint: disable=too-few-public-methods
    """
    Форма для ввода данных доставки.
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Форма для ввода данных доставки.
        """
        model = Delivery
        fields = ['address', 'info']
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}
            ),
            'info': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация'}
            ),
        }
        labels = {
            'address': 'Адрес доставки',
            'info': 'Дополнительная информация (необязательно)',
        }
