from aiogram import Router
from . import user, admin


def get_handlers_router() -> Router:
    """
    Combines all feature routers (user, admin, etc.) into one main router.
    """
    router = Router()
    router.include_router(user.router)
    router.include_router(admin.router)
    return router
