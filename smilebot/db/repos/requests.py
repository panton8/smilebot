from datetime import date, time

from psycopg import AsyncConnection
from psycopg.rows import class_row

from smilebot.domain.models import SearchRequest

CREATE_SQL = """
INSERT INTO search_requests (chat_id, city_from, city_to, trip_date, time_from, time_to)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id;
"""

LIST_ACTIVE_SQL = """
SELECT id, chat_id, city_from, city_to, trip_date, time_from, time_to, status
FROM search_requests
WHERE chat_id = %s AND status IN ('active', 'found')
ORDER BY id;
"""

CLOSE_SQL = """
UPDATE search_requests
SET status = 'closed', closed_at = now()
WHERE id = %s AND chat_id = %s AND status IN ('active', 'found')
RETURNING id;
"""


async def create(
    conn: AsyncConnection,
    *,
    chat_id: int,
    city_from: str,
    city_to: str,
    trip_date: date,
    time_from: time | None,
    time_to: time | None,
) -> int:
    cur = await conn.execute(
        CREATE_SQL,
        (chat_id, city_from, city_to, trip_date, time_from, time_to),
    )
    (request_id,) = await cur.fetchone()
    return request_id


async def list_active(conn: AsyncConnection, chat_id: int) -> list[SearchRequest]:
    async with conn.cursor(row_factory=class_row(SearchRequest)) as cur:
        await cur.execute(LIST_ACTIVE_SQL, (chat_id,))
        return await cur.fetchall()


async def close(conn: AsyncConnection, *, request_id: int, chat_id: int) -> bool:
    """Close a request owned by ``chat_id``; return False if nothing matched."""
    cur = await conn.execute(CLOSE_SQL, (request_id, chat_id))
    return await cur.fetchone() is not None
