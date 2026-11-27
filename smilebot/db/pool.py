import logging
from pathlib import Path

from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent.parent / "migrations"
ADVISORY_LOCK_KEY = 618_0000


def create_pool(dsn: str) -> AsyncConnectionPool:
    """Create a pool (not opened yet); call ``await pool.open()`` to start it."""
    return AsyncConnectionPool(dsn, min_size=1, max_size=5, open=False)


async def apply_migrations(
    pool: AsyncConnectionPool,
    migrations_dir: Path = MIGRATIONS_DIR,
) -> int:
    applied = 0
    async with pool.connection() as conn:
        await conn.execute("SELECT pg_advisory_lock(%s)", (ADVISORY_LOCK_KEY,))
        try:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    name TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            await conn.commit()

            for path in sorted(migrations_dir.glob("*.sql")):
                async with conn.transaction():
                    cur = await conn.execute(
                        "SELECT 1 FROM schema_migrations WHERE name = %s",
                        (path.name,),
                    )
                    if await cur.fetchone() is not None:
                        continue

                    await conn.execute(path.read_text(encoding="utf-8"))
                    await conn.execute(
                        "INSERT INTO schema_migrations (name) VALUES (%s)",
                        (path.name,),
                    )
                    applied += 1
                    logger.info("Applied migration %s", path.name)
        finally:
            await conn.execute("SELECT pg_advisory_unlock(%s)", (ADVISORY_LOCK_KEY,))
            await conn.commit()

    return applied
