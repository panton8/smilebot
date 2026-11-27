from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from psycopg import AsyncConnection

from smilebot.db.repos import requests as requests_repo

router = Router(name="stop")

USAGE = "Invalid format. Use: /stop 39"


@router.message(Command("stop"))
async def cmd_stop(
    message: Message,
    command: CommandObject,
    conn: AsyncConnection,
) -> None:
    args = (command.args or "").strip()
    if not args.isdigit():
        await message.answer(USAGE)
        return

    request_id = int(args)
    closed = await requests_repo.close(
        conn,
        request_id=request_id,
        chat_id=message.chat.id,
    )
    if closed:
        await message.answer(f"Your request {request_id} was successfully closed")
    else:
        await message.answer(f"Request {request_id} was not found or already closed")
