"""
Путь: module_orders/admin.py
Админ-панель для управления моделями приложения module_orders.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from .models import Order, OrderProduct, Delivery

class OrderProductInline(admin.TabularInline):
    """
    Встраиваемая админ-панель для продуктов в заказе.
    """
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

class DeliveryInline(admin.StackedInline):
    """
    Встраиваемая админ-панель для доставки.
    """
    model = Delivery
    extra = 0
    readonly_fields = ('address', 'date', 'info')

class OrderAdmin(admin.ModelAdmin):
    """
    Админ-панель для заказов.
    """
    list_display = ('id', 'user', 'get_username', 'status', 'date', 'delivery_address')
    inlines = [OrderProductInline, DeliveryInline]
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'status')
    list_editable = ('status',)

    def get_username(self, obj):
        """
        Возвращает имя пользователя для отображения в списке заказов.
        """
        return obj.user.username
    get_username.short_description = 'Username'

    def delivery_address(self, obj):
        """
        Возвращает адрес доставки для заказа, если он есть.
        """
        try:
            delivery = Delivery.objects.get(order=obj)  # pylint: disable=no-member
            return delivery.address
        except ObjectDoesNotExist:
            return 'Не указано'
    delivery_address.short_description = 'Адрес доставки'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Delivery)
