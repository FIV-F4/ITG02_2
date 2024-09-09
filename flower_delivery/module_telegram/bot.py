import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from module_telegram.config import TOKEN
from asgiref.sync import sync_to_async
import logging

logging.basicConfig(level=logging.INFO)

# Установка бота
bot = Bot(token=TOKEN)
router = Router()


# Обработчик команды /get_order
@router.message(Command('get_order'))
async def get_order(message: Message):
    from module_telegram.database import get_order_details
    user_id = message.from_user.id

    # Асинхронный вызов функции для получения деталей заказа
    order_details = await sync_to_async(get_order_details)(user_id)

    if order_details:
        await message.answer(f"Ваш заказ:\n{order_details}")
    else:
        await message.answer("У вас нет активных заказов.")


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
    print(message)
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я бот для управления заказами.",
        reply_markup=create_order_keyboard()
    )


# Обработка callback-запроса на получение заказа
@router.callback_query(F.data == "get_order")
async def process_get_order(callback: CallbackQuery):
    from module_telegram.database import get_order_details
    user_id = callback.from_user.id

    # Асинхронный вызов функции для получения деталей заказа
    order_details = await sync_to_async(get_order_details)(user_id)

    if order_details:
        await callback.message.answer(f"Ваш заказ:\n{order_details}")
    else:
        await callback.message.answer("У вас нет активных заказов.")

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
