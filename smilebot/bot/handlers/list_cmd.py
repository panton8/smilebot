from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from psycopg import AsyncConnection

from smilebot.db.repos import requests as requests_repo

router = Router(name="list")


@router.message(Command("list"))
async def cmd_list(message: Message, conn: AsyncConnection) -> None:
    active = await requests_repo.list_active(conn, chat_id=message.chat.id)
    if not active:
        await message.answer("You have no active requests")
        return

    lines = ["Your active requests:"]
    for request in active:
        window = (
            f" {request.time_from:%H:%M}-{request.time_to:%H:%M}"
            if request.time_from and request.time_to
            else ""
        )
        lines.append(
            f"#{request.id} · {request.city_from} -> {request.city_to}"
            f" · {request.trip_date:%d.%m}{window} · {request.status}"
        )
    await message.answer("\n".join(lines))
