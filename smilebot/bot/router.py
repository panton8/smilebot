from aiogram import Router

from smilebot.bot.handlers import list_cmd, request_cmd, start, stop_cmd


def build_router() -> Router:
    router = Router(name="root")
    router.include_routers(
        start.router,
        request_cmd.router,
        list_cmd.router,
        stop_cmd.router,
    )
    return router
