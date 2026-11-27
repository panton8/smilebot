from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="start")

HELP_TEXT = (
    "Commands:\n"
    "/request <from> -> <to> <YYYY-MM-DD> [HH:MM-HH:MM]\n"
    "/list - your active requests\n"
    "/stop <id> - close a request\n\n"
    "Example:\n"
    "/request Rechitsa -> Minsk 2026-12-05 15:00-18:00"
)


@router.message(Command("start", "help"))
async def cmd_start(message: Message) -> None:
    await message.answer(HELP_TEXT)
