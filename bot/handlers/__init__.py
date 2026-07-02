from aiogram import Router
from . import user, admin, get_chat_id

def get_handlers_router() -> Router:
    """
    Combines all feature routers (user, admin, etc.) into one main router.
    """
    router = Router()
    router.include_router(admin.router)
    router.include_router(get_chat_id.router)
    router.include_router(user.router)
    return router
