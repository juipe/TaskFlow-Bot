from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_priority_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="🟢 Низкий",
        callback_data="low_priority"
    ))
    builder.add(types.InlineKeyboardButton(
        text="🟡 Средний",
        callback_data="middle_priority"
    ))
    builder.add(types.InlineKeyboardButton(
        text="🔴 Высокий",
        callback_data="high_priority"
    ))
    builder.adjust(1)
    return builder.as_markup()
