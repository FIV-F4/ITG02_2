"""
Путь: module_catalog/models.py
Модели для приложения module_catalog.
"""

from django.db import models

class Products(models.Model):
    """
    Модель для продукта в каталоге.
    Поля:
    - name: Название продукта.
    - price: Цена продукта.
    - image: Изображение продукта.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/products')

# Пример создания продукта:
# from module_catalog.models import Products
#
# product = Products.objects.create(
#     name='Роза',
#     price=50.00,
#     image='images/products/rose.jpg'
# )
#
# print(product.id, product.name, product.price, product.image.url)

# Добавлена новая строка в конце файла.
