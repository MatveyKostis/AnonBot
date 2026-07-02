from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """
    Handles /admin command (placeholder).
    In production, you'd restrict this using a custom filter or admin ID list.
    """
    await message.answer("Welcome to the Admin panel. Currently, no admin tasks are configured.")
