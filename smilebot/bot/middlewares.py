from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from psycopg_pool import AsyncConnectionPool


class DbMiddleware(BaseMiddleware):
    """Inject a pooled connection into handlers and commit on success.

    If the handler raises, no commit happens and the pool rolls the
    transaction back when the connection is returned.
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.pool.connection() as conn:
            data["conn"] = conn
            result = await handler(event, data)
            await conn.commit()
            return result
