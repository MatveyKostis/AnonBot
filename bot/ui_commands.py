from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_commands(bot: Bot):
    """
    Sets default commands in the Telegram client's command menu.
    """
    commands = [
        BotCommand(command="start", description="Start Frankenstein Bot"),
        BotCommand(command="help", description="Show help information"),
        BotCommand(command="about", description="About the bot"),
        BotCommand(command="admin", description="Admin panel placeholder"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
