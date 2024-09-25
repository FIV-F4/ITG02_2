"""
Путь: module_orders/views.py
Представления для управления заказами, корзиной и доставкой.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from module_catalog.models import Products
from module_telegram.bot import notify_order_status  # Исправлен порядок импортов
from .models import Order, OrderProduct
from .forms import DeliveryForm


@login_required
def cart_view(request):
    """
    Отображает корзину пользователя.
    """
    order = Order.objects.filter(user=request.user, status='cart').first()  # pylint: disable=no-member
    order_products = OrderProduct.objects.filter(order=order) if order else []  # pylint: disable=no-member
    total_price = sum(product.price * product.quantity for product in order_products)  # pylint: disable=no-member

    context = {
        'order': order,
        'order_products': order_products,
        'total_price': total_price
    }
    return render(request, 'module_orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """
    Добавляет продукт в корзину пользователя.
    """
    product = get_object_or_404(Products, id=product_id)
    order, _ = Order.objects.get_or_create(user=request.user, status='cart')  # pylint: disable=no-member
    order_product, created = OrderProduct.objects.get_or_create(  # pylint: disable=no-member
        order=order, product=product, defaults={'price': product.price}
    )
    if created:
        order_product.quantity = 1
    else:
        order_product.quantity += 1
    order_product.save()
    return redirect('cart')


@login_required
def checkout_view(request):
    """
    Оформление заказа и ввод информации о доставке.
    """
    order = Order.objects.filter(user=request.user, status='cart').first()  # pylint: disable=no-member

    if not order:
        return redirect('cart')

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
    """
    Подтверждение заказа после его оформления.
    """
    # pylint: disable=unused-argument
    order = Order.objects.get(id=order_id, user=request.user)  # pylint: disable=no-member
    return render(request, 'module_orders/order_confirmation.html', {"order": order})


@login_required
def order_list_view(request):
    """
    Отображает список заказов пользователя, кроме заказов со статусом 'Корзина'.
    """
    orders = Order.objects.filter(user=request.user).exclude(status='cart').order_by('-date')  # pylint: disable=no-member
    order_products = []
    for order in orders:
        products = OrderProduct.objects.filter(order=order)  # pylint: disable=no-member
        order_products.append((order, products))

    context = {
        'order_products': order_products,
    }
    return render(request, 'module_orders/order_list.html', context)


@login_required
def update_order_status(order_id, new_status):
    """
    Обновляет статус заказа и отправляет уведомление.
    """
    from asgiref.sync import async_to_sync  # pylint: disable=import-outside-toplevel
    order = Order.objects.get(id=order_id)  # pylint: disable=no-member
    order.status = new_status
    order.save()

    async_to_sync(notify_order_status)(order_id, new_status)
    return redirect('order_list')
