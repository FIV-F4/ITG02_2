"""
Путь: module_telegram/database.py
Функции для работы с базой данных заказов и пользователей.
"""

from module_orders.models import Order
from module_reg_auth_user.models import User

def get_order_details(user_id):
    """
    Получает детали заказов для указанного пользователя.
    """
    orders = Order.objects.filter(user_id=user_id)  # pylint: disable=no-member
    if not orders.exists():
        return None

    order_details = []
    for order in orders:
        products = order.orderproduct_set.all()  # pylint: disable=no-member
        details = {
            'order_id': order.id,
            'status': order.get_status_display(),
            'date': order.date,
            'products': [
                {
                    'name': product.product.name,
                    'quantity': product.quantity,
                    'price': product.price,
                }
                for product in products
            ]
        }
        order_details.append(details)

    return order_details

def get_order_user(order_id):
    """
    Получает идентификатор пользователя, оформившего заказ.
    """
    order = Order.objects.get(id=order_id)  # pylint: disable=no-member
    return order.user_id

def update_order_status(order_id, new_status):
    """
    Обновляет статус заказа.
    """
    try:
        order = Order.objects.get(id=order_id)  # pylint: disable=no-member
        order.status = new_status
        order.save()
    except Order.DoesNotExist:  # pylint: disable=no-member
        pass

def get_order_report():
    """
    Генерирует отчёт по заказам.
    """
    total_orders = Order.objects.count()  # pylint: disable=no-member
    total_ordered = Order.objects.filter(status='ordered').count()  # pylint: disable=no-member
    total_shipped = Order.objects.filter(status='shipped').count()  # pylint: disable=no-member
    total_delivered = Order.objects.filter(status='delivered').count()  # pylint: disable=no-member

    report = (
        f"Всего заказов: {total_orders}\n"
        f"Оформлено: {total_ordered}\n"
        f"Отправлено: {total_shipped}\n"
        f"Доставлено: {total_delivered}"
    )
    return report if total_orders > 0 else None

def get_user_id_by_telegram_id(telegram_id):
    """
    Получает идентификатор пользователя по его Telegram ID.
    """
    try:
        user = User.objects.get(telegram_id=telegram_id)  # pylint: disable=no-member
        return user.id
    except User.DoesNotExist:  # pylint: disable=no-member
        return None

def get_last_order_details(user_id):
    """
    Получает детали последнего заказа для указанного пользователя.
    """
    order = Order.objects.filter(user_id=user_id).order_by('-date').first()
    if not order:
        return None
    products = order.orderproduct_set.all()
    details = {
        'order_id': order.id,
        'status': order.get_status_display(),
        'date': order.date,
        'products': [
            {
                'name': product.product.name,
                'quantity': product.quantity,
                'price': product.price,
            }
            for product in products
        ]
    }
    return details

def get_orders_by_status(statuses):
    """
    Получает все заказы с указанными статусами.
    """
    orders = Order.objects.filter(status__in=statuses)
    if not orders.exists():
        return None
    order_details = []
    for order in orders:
        products = order.orderproduct_set.all()
        details = {
            'order_id': order.id,
            'status': order.get_status_display(),
            'date': order.date,
            'products': [
                {
                    'name': product.product.name,
                    'quantity': product.quantity,
                    'price': product.price,
                }
                for product in products
            ]
        }
        order_details.append(details)
    return order_details
