"""
Путь: module_catalog/admin.py
Админ-панель для управления моделями приложения module_catalog.
"""
from django.contrib import admin
from .models import Products
from django.utils.html import format_html

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        else:
            return "Нет изображения"

    image_preview.short_description = 'Предпросмотр изображения'

