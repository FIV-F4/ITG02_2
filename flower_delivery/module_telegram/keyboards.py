"""
Путь: module_telegram/keyboards.py
Функции для создания клавиатуры в Telegram-боте.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_order_keyboard(is_admin=False):
    """
    Создает клавиатуру для управления заказами.
    """
    keyboard = [
        [InlineKeyboardButton(text="Последний заказ", callback_data="get_last_order")],
        [InlineKeyboardButton(text="Все заказы", callback_data="get_order")],
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton(text="Отчёт", callback_data="order_report")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

