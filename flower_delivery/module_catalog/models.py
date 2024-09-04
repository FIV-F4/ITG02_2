from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/products')
# Create your models here.

'''
from module_catalog.models import Products

# Создание продукта
product = Products.objects.create(
    name='Роза',
    price=50.00,
    image='images/products/rose.jpg'
)

# Печать информации о продукте
print(product.id, product.name, product.price, product.image.url)
'''