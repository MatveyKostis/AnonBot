from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Creates the main menu reply keyboard markup.
    """
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Help ❓"))
    builder.add(KeyboardButton(text="About ℹ️"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
