import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import get_handlers_router
from bot.middlewares import LoggingMiddleware, I18nMiddleware
from bot.utils.db import db
from bot.ui_commands import set_bot_commands

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Initializing Frankenstein Bot...")

    # Initialize Bot instance with default HTML parsing mode
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Initialize Dispatcher
    dp = Dispatcher()

    # Register middlewares (e.g. LoggingMiddleware)
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(I18nMiddleware())

    # Register routers (handlers)
    dp.include_router(get_handlers_router())

    # Startup Hook
    # Triggered before the dispatcher begins polling
    @dp.startup()
    async def on_startup(bot: Bot):
        logger.info("Bot starting up. Registering command menu...")
        await set_bot_commands(bot)
        logger.info("Commands registered. Ready to receive updates.")

    # Shutdown Hook (Graceful termination support)
    # When systemd sends SIGTERM or manual stop sends SIGINT, aiogram catches it,
    # stops polling, and fires this shutdown sequence.
    @dp.shutdown()
    async def on_shutdown(bot: Bot):
        logger.warning("Shutdown signal received (SIGINT/SIGTERM from systemd). Cleaning up...")
        
        # Close bot HTTP session to release resources
        await bot.session.close()
        
        logger.info("Resources cleaned up. Bot session closed.")

    # Start Polling
    # handle_signals=True is enabled by default in aiogram.
    # It catches SIGINT and SIGTERM, stopping the dispatcher loop gracefully.
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.critical("Unexpected error in bot main loop: %s", e, exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Frankenstein Bot execution stopped.")
