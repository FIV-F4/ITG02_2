# module_orders/admin.py

from django.contrib import admin
from .models import Order, OrderProduct, Delivery
from django.core.exceptions import ObjectDoesNotExist

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0  # Показывать существующие продукты, без добавления новых строк
    readonly_fields = ('product', 'quantity', 'price')  # Только для чтения

class DeliveryInline(admin.StackedInline):
        model = Delivery
        extra = 0  # Показывать существующую доставку, без добавления новых строк
        readonly_fields = ('address', 'date', 'info')  # Только для чтения

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'date','delivery_address')
    inlines = [OrderProductInline, DeliveryInline]
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'status')
    list_editable = ('status',)

    def delivery_address(self, obj):
        try:
            delivery = Delivery.objects.get(order=obj)
            return delivery.address
        except ObjectDoesNotExist:
            return 'Не указано'
    delivery_address.short_description = 'Адрес доставки'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Delivery)
