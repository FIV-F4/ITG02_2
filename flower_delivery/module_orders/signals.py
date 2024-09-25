# module_orders/signals.py

import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from module_orders.models import Order
from module_reg_auth_user.models import User
from module_telegram.bot import TOKEN
from asgiref.sync import async_to_sync
from aiogram import exceptions
import logging
from aiogram import Bot

async def send_message(telegram_id, message):
    """
    Асинхронно отправляет сообщение пользователю по telegram_id.
    """
    print('Отправка сообщения...')
    bot_token = TOKEN
    try:
        async with Bot(token=bot_token) as bot:
            await bot.send_message(telegram_id, message)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения пользователю с telegram_id {telegram_id}: {e}")

@receiver(post_save, sender=Order)
def notify_on_order_status_change(sender, instance, **kwargs):
    """
    Уведомляет администраторов и покупателя при изменении статуса заказа.
    """
    if not instance.pk:  # Если заказ только что создан
        return

    # Проверяем, изменился ли статус заказа и он не равен 'cart'
    if 'status' in instance.__dict__ and instance.status != 'cart':
        # Формируем сообщение с информацией о заказе и доставке
        message = f"🆕 Новый статус заказа #{instance.id}: {instance.get_status_display()}\n"
        message += f"📦 Продукты:\n"
        for order_product in instance.orderproduct_set.all():
            message += f" - {order_product.product.name} (x{order_product.quantity})\n"
        # Форматируем дату без долей секунды и часового пояса
        formatted_date = instance.date.strftime('%Y-%m-%d %H:%M:%S')
        message += f"📅 Дата: {formatted_date}\n"

        if instance.delivery_set.exists():
            delivery = instance.delivery_set.first()  # Предполагаем, что для заказа есть только одна доставка
            message += f"🚚 Адрес доставки: {delivery.address}\n"
            message += f"📞 Дополнительная информация: {delivery.info}\n"
        else:
            message += "Информация о доставке отсутствует.\n"

        # Получаем всех администраторов с указанным telegram_id
        admins = User.objects.filter(is_staff=True, telegram_id__isnull=False)

        # Отправляем уведомление администраторам
        for admin in admins:
            try:
                async_to_sync(send_message)(admin.telegram_id, message)
                print(f"Отправлено сообщение администратору с telegram_id {admin.telegram_id}")
            except exceptions.TelegramBadRequest as e:
                logging.error(f"Не удалось отправить сообщение администратору с telegram_id {admin.telegram_id}: {e}")

        # Отправляем уведомление покупателю
        buyer = instance.user
        if buyer.telegram_id:
            try:
                async_to_sync(send_message)(buyer.telegram_id, message)
                print(f"Отправлено сообщение покупателю с telegram_id {buyer.telegram_id}")
            except exceptions.TelegramBadRequest as e:
                logging.error(f"Не удалось отправить сообщение покупателю с telegram_id {buyer.telegram_id}: {e}")
        else:
            print(f"У пользователя {buyer.username} не указан telegram_id, уведомление не отправлено.")
