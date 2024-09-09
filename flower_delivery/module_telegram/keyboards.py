# keyboards.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_order_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Получить заказ", callback_data="get_order")],
            [InlineKeyboardButton(text="Отчёт", callback_data="order_report")]
        ]
    )
