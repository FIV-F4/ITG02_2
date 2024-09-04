# module_orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from module_catalog.models import Products
from .forms import DeliveryForm
from django.db.models import Prefetch
from django.contrib import messages

@login_required
def cart_view(request):
    # Получаем текущий заказ со статусом "Корзина" для текущего пользователя
    order = Order.objects.filter(user=request.user, status='cart').first()
    order_products = OrderProduct.objects.filter(order=order) if order else []
    total_price = sum([product.price * product.quantity for product in order_products])

    context = {
        'order': order,
        'order_products': order_products,
        'total_price': total_price
    }
    return render(request, 'module_orders/cart.html', context)





@login_required
def add_to_cart(request, product_id):
    # Получаем продукт по ID
    product = get_object_or_404(Products, id=product_id)

    # Получаем текущий заказ со статусом "Корзина" для текущего пользователя
    order, created = Order.objects.get_or_create(user=request.user, status='cart')

    # Проверяем, есть ли уже этот товар в заказе
    order_product, created = OrderProduct.objects.get_or_create(order=order, product=product,defaults={'price': product.price})

    if created:
        order_product.quantity = 1  # Если это новый товар в заказе
    else:
        order_product.quantity += 1  # Если товар уже есть, увеличиваем количество

    order_product.price = product.price
    order_product.save()

    return redirect('cart')


@login_required
def checkout_view(request):
    order = Order.objects.filter(user=request.user, status='cart').first()

    if not order:
        return redirect('cart')  # Если нет заказа в корзине, перенаправляем на страницу корзины

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.order = order
            delivery.save()

            order.status = 'ordered'
            order.save()

            return redirect('order_confirmation', order_id=order.id)
    else:
        form = DeliveryForm()

    return render(request, 'module_orders/checkout.html', {'form': form})
@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "module_orders/order_confirmation.html", {"order": order})


def order_list_view2(request):
    orders = Order.objects.exclude(status='cart').order_by('-date')  # Заказы со всеми статусами, кроме 'cart'

    # Получаем продукты для каждого заказа
    order_products = {}
    for order in orders:
        order_products[order.id] = order.orderproduct_set.all()

    return render(request, 'module_orders/order_list.html', {
        'orders': orders,
        'order_products': order_products,
    })





def order_list_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='cart').order_by('-date')
    order_products = []
    for order in orders:
        products = OrderProduct.objects.filter(order=order)
        order_products.append((order, products))

    context = {
        'order_products': order_products,
    }
    return render(request, 'module_orders/order_list.html', context)
