import os
import asyncio
import django

# Устанавливаем переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

from aiogram import Dispatcher
from module_telegram.bot import bot, router

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
