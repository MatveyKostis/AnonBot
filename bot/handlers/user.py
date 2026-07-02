from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import get_links_keyboard
from bot.keyboards.reply import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handles /start command. Greets user and sends the main reply menu.
    """
    await message.answer(
        f"Hello, {message.from_user.full_name}! Welcome to Frankenstein Bot.\n"
        f"This bot is bootstrapped with a modular and clean structure.",
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("help"))
@router.message(F.text == "Help ❓")
async def cmd_help(message: Message):
    """
    Handles /help command or 'Help ❓' reply keyboard button click.
    """
    await message.answer(
        "Here is what I can do:\n"
        "/start - Start the bot\n"
        "/help - Get help information\n"
        "/about - Learn more about the bot",
        reply_markup=get_links_keyboard(),
    )


@router.message(Command("about"))
@router.message(F.text == "About ℹ️")
async def cmd_about(message: Message):
    """
    Handles /about command or 'About ℹ️' reply keyboard button click.
    """
    await message.answer(
        "Frankenstein Bot is a high-performance Python Telegram bot built on aiogram v3, "
        "designed to work seamlessly with systemd process management."
    )


@router.callback_query(F.data == "support_contact")
async def process_support_callback(callback: CallbackQuery):
    """
    Processes the inline keyboard callback query 'support_contact'.
    """
    await callback.message.answer("Support: Open an issue or contact our administrator.")
    await callback.answer()
