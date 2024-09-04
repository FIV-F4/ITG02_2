# module_orders/urls.py
from django.urls import path
from .views import cart_view, add_to_cart, checkout_view, order_confirmation, order_list_view

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('orders/', order_list_view, name='order_list'),
]
