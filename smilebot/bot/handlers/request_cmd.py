import logging
from datetime import date

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from psycopg import AsyncConnection

from smilebot.db.repos import requests as requests_repo
from smilebot.domain.request_parser import UsageError, parse_request_args

router = Router(name="request")
logger = logging.getLogger(__name__)

USAGE = "Invalid format. Use: /request Rechitsa -> Minsk 2026-12-05 15:00-18:00"


@router.message(Command("request"))
async def cmd_request(
    message: Message,
    command: CommandObject,
    conn: AsyncConnection,
) -> None:
    if not command.args:
        await message.answer(USAGE)
        return

    try:
        parsed = parse_request_args(command.args, today=date.today())
    except UsageError as exc:
        await message.answer(f"{USAGE}\n\n{exc}")
        return

    request_id = await requests_repo.create(
        conn,
        chat_id=message.chat.id,
        city_from=parsed.city_from,
        city_to=parsed.city_to,
        trip_date=parsed.trip_date,
        time_from=parsed.time_from,
        time_to=parsed.time_to,
    )
    logger.info("Created request %s for chat %s", request_id, message.chat.id)
    await message.answer(f"Your request {request_id} is processing...")
