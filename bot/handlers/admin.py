from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings
from bot.utils.db import db
from bot.utils.i18n import _

router = Router()

# Simple middleware-like check for admin
def is_admin(message: Message):
    return message.from_user.id in settings.admins

@router.message(Command("stats"), F.from_user.id.in_(settings.admins))
async def cmd_stats(message: Message, locale: str):
    stats = db.get_stats()
    await message.answer(_("stats_title", locale=locale) + "\n" + _("total_users", locale=locale, count=stats["user_count"]))

@router.message(Command("logs"), F.from_user.id.in_(settings.admins))
async def cmd_logs(message: Message, locale: str):
    logs = db.get_recent_messages()
    if not logs:
        await message.answer(_("no_logs", locale=locale))
        return
    
    response = _("recent_messages", locale=locale) + "\n"
    for log in logs:
        response += f"ID: {log[0]} | {log[1]}: {log[2][:20]}... ({log[3]})\n"
    
    await message.answer(response)

@router.message(Command("view"), F.from_user.id.in_(settings.admins))
async def cmd_view(message: Message, locale: str):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Usage: /view [msg_id]")
        return
    
    msg_id = int(args[1])
    log = db.get_message_details(msg_id)
    if not log:
        await message.answer(_("msg_not_found", locale=locale, id=msg_id))
        return
    
    # log: (id, full_name, username, user_id, content_type, timestamp, text)
    await message.answer(_("msg_details", 
                           locale=locale,
                           id=log[0], 
                           full_name=log[1], 
                           username=log[2], 
                           user_id=log[3], 
                           content_type=log[4], 
                           timestamp=log[5], 
                           text=log[6]))

@router.message(Command("ban"), F.from_user.id.in_(settings.admins))
async def cmd_ban(message: Message, locale: str):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Usage: /ban [user_id]")
        return
    
    user_id = int(args[1])
    db.ban_user(user_id)
    await message.answer(_("user_banned", locale=locale, user_id=user_id))

@router.message(Command("unban"), F.from_user.id.in_(settings.admins))
async def cmd_unban(message: Message, locale: str):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Usage: /unban [user_id]")
        return
    
    user_id = int(args[1])
    db.unban_user(user_id)
    await message.answer(_("user_unbanned", locale=locale, user_id=user_id))
