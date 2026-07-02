from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils.i18n import _

router = Router()

@router.message(Command("id"))
async def cmd_id(message: Message, locale: str):
    await message.answer(_("id_command", locale=locale, id=message.chat.id))
