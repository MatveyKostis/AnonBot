import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """
    A simple middleware that logs details about incoming events.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        logger.debug("Received event: %s", event.__class__.__name__)
        try:
            result = await handler(event, data)
            logger.debug("Event %s handled successfully", event.__class__.__name__)
            return result
        except Exception as e:
            logger.error("Error handling event %s: %s", event.__class__.__name__, e, exc_info=True)
            raise e
