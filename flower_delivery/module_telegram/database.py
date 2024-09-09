from module_orders.models import Order
from module_reg_auth_user.models import User


def get_order_details(user_id):
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


def get_order_user(order_id):
    order = Order.objects.get(id=order_id)
    return order.user_id
