import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from module_telegram.config import TOKEN
from asgiref.sync import sync_to_async
import logging
from datetime import datetime
from decimal import Decimal
from module_telegram.database import get_order_details, get_user_id_by_telegram_id

logging.basicConfig(level=logging.INFO)

# Установка бота
bot = Bot(token=TOKEN)
router = Router()
def format_order_details(order_details):
    if not order_details:
        return "У вас нет активных заказов."

    message = "📦 *Ваши заказы:*\n"
    for order in order_details:
        # Форматирование даты
        if isinstance(order['date'], datetime):
            formatted_date = order['date'].strftime('%d-%m-%Y %H:%M')
        else:
            formatted_date = str(order['date'])

        message += f"\n*Заказ №{order['order_id']}* - _{order['status']}_\n"
        message += f"🗓 *Дата:* {formatted_date}\n"
        message += "🛍 *Товары:*\n"
        for product in order['products']:
            # Форматирование цены
            if isinstance(product['price'], Decimal):
                price = f"{product['price']:.2f}"
            else:
                price = str(product['price'])
            message += f"  • {product['name']} (x{product['quantity']}): *{price} руб.*\n"
        message += "---------------------\n"
    return message





# Обработчик команды /get_order
# Обработчик команды /get_order
@router.message(Command('get_order'))
async def get_order(message: Message):
    user_id = message.from_user.id  # Получение telegram_id
    # Получаем user_id из telegram_id
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_id)

    if not user_id:
        await message.answer("Пользователь не найден.")
        return

    # Асинхронный вызов функции для получения деталей заказа
    order_details = await sync_to_async(get_order_details)(user_id)

    # Форматируем заказ с помощью format_order_details
    formatted_message = format_order_details(order_details)

    await message.answer(formatted_message)


# Функция уведомления пользователя о статусе заказа
async def notify_order_status(order_id, status):
    from module_telegram.database import get_order_user

    # Асинхронный вызов функции для получения user_id по order_id
    user_id = await sync_to_async(get_order_user)(order_id)

    await bot.send_message(user_id, f"Статус вашего заказа #{order_id} изменён на '{status}'.")


# Обработчик команды /update_order
@router.message(Command('update_order'))
async def update_order(message: Message):
    from module_telegram.database import update_order_status
    order_id = int(message.get_args())
    new_status = "ordered"

    # Асинхронное обновление статуса заказа
    await sync_to_async(update_order_status)(order_id, new_status)

    await notify_order_status(order_id, new_status)
    await message.answer(f"Статус заказа #{order_id} изменён на '{new_status}'.")


# Обработчик команды /order_report
@router.message(Command('order_report'))
async def order_report(message: Message):
    from module_telegram.database import get_order_report

    # Асинхронный вызов функции для получения отчёта
    report = await sync_to_async(get_order_report)()

    if report:
        await message.answer(f"Аналитика заказов:\n{report}")
    else:
        await message.answer("Нет данных для отчёта.")


# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message):
    from module_telegram.keyboards import create_order_keyboard
    from module_reg_auth_user.models import User  # Импортируем вашу модель User
    from asgiref.sync import sync_to_async  # Для асинхронного доступа к базе данных

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name

    # Асинхронный вызов Django ORM для проверки наличия пользователя с таким telegram_id
    user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()

    if user:
        # Если у пользователя уже есть telegram_id, приветствуем и показываем меню
        await message.answer(
            f"Привет, {full_name}! Я бот для управления заказами.{user}",
            reply_markup=create_order_keyboard()
        )
    else:
        # Если у пользователя нет telegram_id, отправляем сообщение с просьбой добавить его на сайте
        await message.answer(
            f"Привет, {full_name}! Ваш Telegram ID: {telegram_id}. Пожалуйста, введите этот ID на нашем сайте, чтобы связать ваш аккаунт."
        )


# Обработка callback-запроса на получение заказа
# Обработка callback-запроса на получение заказа
@router.callback_query(F.data == "get_order")
async def process_get_order(callback: CallbackQuery):
    user_telegram_id = callback.from_user.id

    # Получаем user_id на основе telegram_id
    user_id = await sync_to_async(get_user_id_by_telegram_id)(user_telegram_id)

    if not user_id:
        await callback.message.answer("Пользователь не найден.")
        await callback.answer()
        return

    # Асинхронный вызов функции для получения деталей заказа
    order_details = await sync_to_async(get_order_details)(user_id)

    # Форматируем заказ с помощью format_order_details
    formatted_message = format_order_details(order_details)

    await callback.message.answer(formatted_message, parse_mode='Markdown')

    await callback.answer()


# Обработка callback-запроса на получение отчёта
@router.callback_query(F.data == "order_report")
async def process_order_report(callback: CallbackQuery):
    from module_telegram.database import get_order_report

    # Асинхронный вызов функции для получения отчёта
    report = await sync_to_async(get_order_report)()

    if report:
        await callback.message.answer(f"Аналитика заказов:\n{report}")
    else:
        await callback.message.answer("Нет данных для отчёта.")

    await callback.answer()




# Основная функция запуска бота
async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # Запуск polling для бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
