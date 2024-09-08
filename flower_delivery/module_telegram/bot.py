import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from django.conf import settings
from module_orders.models import Order, OrderProduct
from module_catalog.models import Products

# Вставьте сюда ваш API токен Telegram бота
API_TOKEN = 'YOUR_API_TOKEN'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Команда /start для приветствия пользователя
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для отслеживания заказов и получения аналитики по заказам.")


# Команда для получения списка заказов
@dp.message_handler(commands=['orders'])
async def list_orders(message: types.Message):
    user_orders = Order.objects.filter(user__username=message.from_user.username)
    if user_orders.exists():
        response = "Ваши заказы:\n"
        for order in user_orders:
            response += f"\nЗаказ #{order.id} - Статус: {order.get_status_display()}\n"
            for order_product in OrderProduct.objects.filter(order=order):
                response += f"  Продукт: {order_product.product.name} - Количество: {order_product.quantity}\n"
        await message.reply(response)
    else:
        await message.reply("У вас нет заказов.")


# Команда для получения аналитики по заказам
@dp.message_handler(commands=['analytics'])
async def order_analytics(message: types.Message):
    total_orders = Order.objects.count()
    total_delivered = Order.objects.filter(status='delivered').count()
    total_cancelled = Order.objects.filter(status='cancelled').count()

    response = (f"Аналитика по заказам:\n"
                f"Всего заказов: {total_orders}\n"
                f"Доставлено: {total_delivered}\n"
                f"Отменено: {total_cancelled}\n")

    await message.reply(response)


# Уведомления о смене статуса заказа
async def notify_status_change(order_id):
    order = Order.objects.get(id=order_id)
    user = order.user
    status = order.get_status_display()

    await bot.send_message(user.telegram_id, f"Ваш заказ #{order.id} теперь имеет статус: {status}")


# Запуск бота
def start_bot():
    executor.start_polling(dp, skip_updates=True)
