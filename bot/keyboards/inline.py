from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_links_keyboard() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup with external links and callback query button.
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Google", url="https://google.com"))
    builder.add(InlineKeyboardButton(text="Contact Support 💬", callback_data="support_contact"))
    builder.adjust(1)
    return builder.as_markup()
