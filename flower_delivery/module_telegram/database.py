from module_orders.models import Order
from module_reg_auth_user.models import User


# Функция для получения деталей заказа по user_id
def get_order_details(user_id):
    #user_id = get_user_id_by_telegram_id(user_id)
    orders = Order.objects.filter(user_id=user_id)
    if not orders.exists():
        return None

    order_details = []
    for order in orders:
        products = order.orderproduct_set.all()
        details = {
            'order_id': order.id,
            'status': order.get_status_display(),
            'date': order.date,
            'products': [{
                'name': product.product.name,
                'quantity': product.quantity,
                'price': product.price,
            } for product in products]
        }
        order_details.append(details)

    return order_details


# Функция для получения user_id по order_id
def get_order_user(order_id):
    order = Order.objects.get(id=order_id)
    return order.user_id


# Функция для обновления статуса заказа
def update_order_status(order_id, new_status):
    try:
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
    except Order.DoesNotExist:
        pass


# Функция для получения отчёта по заказам
def get_order_report():
    # Например, возвращаем общее количество заказов
    total_orders = Order.objects.count()
    total_ordered = Order.objects.filter(status='ordered').count()
    total_shipped = Order.objects.filter(status='shipped').count()
    total_delivered = Order.objects.filter(status='delivered').count()

    report = (
        f"Всего заказов: {total_orders}\n"
        f"Оформлено: {total_ordered}\n"
        f"Отправлено: {total_shipped}\n"
        f"Доставлено: {total_delivered}"
    )
    return report if total_orders > 0 else None


# Функция для получения user_id по telegram_id
def get_user_id_by_telegram_id(telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        return user.id
    except User.DoesNotExist:
        return None
