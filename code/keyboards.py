from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


builder = InlineKeyboardBuilder()

builder.row(
    InlineKeyboardButton(
        text="УникУм",
        callback_data="unikum")
    ,InlineKeyboardButton(
        text="КузГТУ",
        callback_data="kuzgtu")
)

organizations_keyboard = builder.as_markup()
