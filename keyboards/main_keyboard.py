from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# main keyboard
def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="📋 Мои задачи", style='success')],
        [KeyboardButton(text="➕ Добавить задачу", style='primary')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
