from django import forms
from .models import Order, Delivery


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['address', 'info']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация'}),
        }
        labels = {
            'address': 'Адрес доставки',
            'info': 'Дополнительная информация (необязательно)',
        }