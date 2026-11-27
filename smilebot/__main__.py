import asyncio
import logging

from aiogram import Bot, Dispatcher

from smilebot.bot.middlewares import DbMiddleware
from smilebot.bot.router import build_router
from smilebot.config import get_settings
from smilebot.db.pool import apply_migrations, create_pool
from smilebot.logging import setup_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    pool = create_pool(settings.db_dsn)
    await pool.open()
    logger.info("Database pool is open")

    try:
        applied = await apply_migrations(pool)
        logger.info("Migrations applied: %d", applied)

        bot = Bot(token=settings.bot_token)
        dp = Dispatcher()
        dp.update.middleware(DbMiddleware(pool))
        dp.include_router(build_router())

        logger.info("Starting polling")
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
            logger.info("Bot session closed")
    finally:
        await pool.close()
        logger.info("Database pool closed")


if __name__ == "__main__":
    asyncio.run(main())
