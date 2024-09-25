"""
Путь: module_telegram/bot.py
Telegram-бот для управления заказами.
"""

import asyncio
import logging
from datetime import datetime
from decimal import Decimal
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from asgiref.sync import sync_to_async
from module_telegram.config import TOKEN
from module_telegram.database import (
    get_order_details, get_user_id_by_telegram_id, get_order_user,
    update_order_status, get_order_report, get_last_order_details
)
from module_telegram.keyboards import create_order_keyboard
from module_reg_auth_user.models import User
from module_analytics.reports import generate_detailed_report


logging.basicConfig(level=logging.INFO)

# Установка бота
bot = Bot(token=TOKEN)
router = Router()

def format_order_details(order_details):
    """
    Форматирует детали заказа для отображения в сообщении.
    Разбивает длинные сообщения на части, если они превышают лимит Telegram.
    """
    if not order_details:
        return ["У вас нет активных заказов."]

    messages = []
    current_message = "📦 *Ваши заказы:*\n"
    for order in order_details:
        formatted_date = (
            order['date'].strftime('%d-%m-%Y %H:%M')
            if isinstance(order['date'], datetime)
            else str(order['date'])
        )
        order_message = (
            f"\n*Заказ №{order['order_id']}* - _{order['status']}_\n"
            f"🗓 *Дата:* {formatted_date}\n"
            "🛍 *Товары:*\n"
        )
        for product in order['products']:
            price = (
                f"{product['price']:.2f}" if isinstance(product['price'], Decimal)
                else str(product['price'])
            )
            order_message += (
                f"  • {product['name']} (x{product['quantity']}): *{price} руб.*\n"
            )
        order_message += "---------------------\n"

        # Проверяем, не превышает ли текущее сообщение лимит
        if len(current_message) + len(order_message) > 4000:
            messages.append(current_message)
            current_message = order_message
        else:
            current_message += order_message

    # Добавляем оставшееся сообщение
    if current_message:
        messages.append(current_message)
    return messages


# Обработчик команды /get_order


# Функция уведомления пользователя о статусе заказа
# Функция уведомления пользователя о статусе заказа
async def notify_order_status(order_id, status):
    """
    Уведомляет пользователя и администраторов о изменении статуса заказа.
    """
    # Уведомление пользователя
    user_id = await sync_to_async(get_order_user)(order_id)
    await bot.send_message(user_id, f"Статус вашего заказа #{order_id} изменён на '{status}'.")

    # Уведомление администраторов
    admins = await sync_to_async(User.objects.filter(is_staff=True, telegram_id__isnull=False).all)()

    if admins:
        message = f"🆕 Изменение статуса заказа #{order_id} на '{status}'."
        for admin in admins:
            await bot.send_message(admin.telegram_id, message)
# Обработчик команды /update_order
@router.message(Command('update_order'))
async def update_order(message: Message):
    """
    Обновляет статус заказа.
    """
    order_id = int(message.get_args())
    new_status = "ordered"

    # Асинхронное обновление статуса заказа
    await sync_to_async(update_order_status)(order_id, new_status)
    await notify_order_status(order_id, new_status)
    await message.answer(f"Статус заказа #{order_id} изменён на '{new_status}'.")

# Обработчик команды /order_report
@router.callback_query(F.data == "order_report")
async def process_order_report(callback: CallbackQuery):
    """
    Обрабатывает запрос на получение подробного отчёта через колбэк.
    """
    user_telegram_id = callback.from_user.id
    user = await sync_to_async(User.objects.filter(telegram_id=user_telegram_id).first)()
    if not user or not user.is_staff:
        await callback.message.answer("У вас нет доступа к этой информации.")
        await callback.answer()
        return

    # Получаем подробный отчёт из модуля аналитики
    report = await sync_to_async(generate_detailed_report)()

    if report:
        messages = split_long_message(report)
        for msg in messages:
            await callback.message.answer(msg)
    else:
        await callback.message.answer("Нет данных для отчёта.")

    await callback.answer()



# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message):
    """
    Приветственное сообщение для нового пользователя.
    """
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name

    # Проверка наличия пользователя с таким telegram_id
    user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()

    if user:
        is_admin = user.is_staff
        await message.answer(
            f"Привет, {full_name}! Я бот для управления заказами.",
            reply_markup=create_order_keyboard(is_admin)
        )
    else:
        await message.answer(
            f"Привет, {full_name}! Ваш Telegram ID: {telegram_id}. "
            "Пожалуйста, введите этот ID на нашем сайте, чтобы связать ваш аккаунт."
        )

# Обработка callback-запроса на получение заказа
# Обработка колбэка для получения последнего заказа


# Обработка колбэка для получения всех заказов
@router.message(Command('get_order'))
async def get_order(message: Message):
    """
    Получает детали заказа для пользователя по его telegram_id.
    """
    user_id = message.from_user.id  # Получение telegram_id
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_id)

    if not user_id:
        await message.answer("Пользователь не найден.")
        return

    order_details = await sync_to_async(get_order_details)(user_id)
    messages = format_order_details(order_details)
    for msg in messages:
        await message.answer(msg, parse_mode='Markdown')

# Обработка колбэка для получения всех заказов
@router.callback_query(F.data == "get_order")
async def process_get_order(callback: CallbackQuery):
    """
    Обрабатывает запрос на получение всех заказов через колбэк.
    """
    user_telegram_id = callback.from_user.id
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_telegram_id)

    if not user_id:
        await callback.message.answer("Пользователь не найден.")
        await callback.answer()
        return

    order_details = await sync_to_async(get_order_details)(user_id)
    messages = format_order_details(order_details)
    for msg in messages:
        await callback.message.answer(msg, parse_mode='Markdown')
    await callback.answer()



# Обработка callback-запроса на получение отчёта
@router.message(Command('order_report'))
async def order_report(message: Message):
    """
    Отправляет подробный отчёт по заказам пользователю (только для администраторов).
    """
    user_telegram_id = message.from_user.id
    user = await sync_to_async(User.objects.filter(telegram_id=user_telegram_id).first)()
    if not user or not user.is_staff:
        await message.answer("У вас нет доступа к этой информации.")
        return

    try:
        report = await sync_to_async(generate_detailed_report)()
    except Exception as e:
        logging.exception("Ошибка при генерации отчёта: %s", e)
        await message.answer("Произошла ошибка при генерации отчёта.")
        return

    if report:
        messages = split_long_message(report)
        for msg in messages:
            await message.answer(msg, parse_mode='Markdown')
    else:
        await message.answer("Нет данных для отчёта.")


def split_long_message(text, max_length=4096):
    """
    Разбивает длинный текст на части, не превышающие max_length символов.
    """
    messages = []
    while len(text) > max_length:
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        messages.append(text[:split_index])
        text = text[split_index:]
    messages.append(text)
    return messages



@router.message(Command('get_last_order'))
async def get_last_order(message: Message):
    """
    Получает детали последнего заказа пользователя.
    """
    user_id = message.from_user.id  # Telegram ID
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_id)
    if not user_id:
        await message.answer("Пользователь не найден.")
        return
    last_order_details = await sync_to_async(get_last_order_details)(user_id)
    if not last_order_details:
        await message.answer("У вас нет заказов.")
        return
    messages = format_order_details([last_order_details])
    for msg in messages:
        await message.answer(msg, parse_mode='Markdown')

# Обработка колбэка для получения последнего заказа
@router.callback_query(F.data == "get_last_order")
async def process_get_last_order(callback: CallbackQuery):
    """
    Обрабатывает запрос на получение последнего заказа через колбэк.
    """
    user_telegram_id = callback.from_user.id
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_telegram_id)

    if not user_id:
        await callback.message.answer("Пользователь не найден.")
        await callback.answer()
        return

    last_order_details = await sync_to_async(get_last_order_details)(user_id)
    if not last_order_details:
        await callback.message.answer("У вас нет заказов.")
        await callback.answer()
        return

    messages = format_order_details([last_order_details])
    for msg in messages:
        await callback.message.answer(msg, parse_mode='Markdown')
    await callback.answer()


@router.message(Command('get_orders_by_status'))
async def get_orders_by_status(message: Message):
    """
    Для администраторов: Получает заказы с определёнными статусами.
    """
    user_telegram_id = message.from_user.id
    user = await sync_to_async(User.objects.filter(telegram_id=user_telegram_id).first)()
    if not user or not user.is_staff:
        await message.answer("У вас нет доступа к этой информации.")
        return

    # Используем статусы по умолчанию, если аргументы не переданы
    statuses = ['ordered', 'Оформлен', 'shipped', 'Отправлен']
    orders = await sync_to_async(get_orders_by_status)(statuses)
    if not orders:
        await message.answer("Нет заказов с указанными статусами.")
        return
    formatted_message = format_order_details(orders)
    await message.answer(formatted_message, parse_mode='Markdown')


# Основная функция запуска бота
async def main():
    """
    Запускает бота и обрабатывает команды.
    """
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
