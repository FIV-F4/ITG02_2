"""
Модуль для запуска Telegram-бота с использованием aiogram и Django ORM.
"""

import os
import asyncio
import django

# Устанавливаем переменную окружения для конфигурации Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

async def main():
    """
    Основная асинхронная функция для запуска бота.
    Она создает диспетчер, подключает маршрутизатор
    и запускает бот в режиме опроса.
    """
    # Импорты, которые зависят от настройки Django
    from aiogram import Dispatcher  # pylint: disable=C0415
    from module_telegram.bot import bot, router  # pylint: disable=C0415

    # Создаем диспетчер для управления событиями бота
    dp = Dispatcher()

    # Подключаем маршрутизатор, который управляет обработкой сообщений
    dp.include_router(router)

    # Запуск опроса для бота (бот будет работать до остановки)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем асинхронный цикл событий
    asyncio.run(main())
