"""Parse the argument line of the /request command.

Format: ``<from> -> <to> <YYYY-MM-DD> [HH:MM-HH:MM]``

Example: ``Rechitsa -> Minsk 2026-12-05 15:00-18:00``
"""

import re
from dataclasses import dataclass
from datetime import date, datetime, time

TIME_WINDOW_RE = re.compile(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$")
ROUTE_SEPARATOR = "->"
DATE_FORMAT = "%Y-%m-%d"


class UsageError(ValueError):
    """Raised when the command arguments cannot be parsed."""


@dataclass(frozen=True, slots=True)
class ParsedRequest:
    city_from: str
    city_to: str
    trip_date: date
    time_from: time | None
    time_to: time | None


def parse_request_args(args: str, *, today: date | None = None) -> ParsedRequest:
    today = today or date.today()
    tokens = args.split()
    if not tokens:
        raise UsageError("arguments are empty")

    time_from: time | None = None
    time_to: time | None = None
    if len(tokens) >= 3 and TIME_WINDOW_RE.match(tokens[-1]):
        raw_from, raw_to = tokens[-1].split("-")
        time_from = _parse_time(raw_from)
        time_to = _parse_time(raw_to)
        if time_from >= time_to:
            raise UsageError("time window start must be before end")
        tokens = tokens[:-1]

    if len(tokens) < 3:
        raise UsageError("expected '<from> -> <to> <YYYY-MM-DD>'")

    trip_date = _parse_date(tokens[-1])
    if trip_date < today:
        raise UsageError("trip date is in the past")

    route = tokens[:-1]
    arrows = [index for index, token in enumerate(route) if token == ROUTE_SEPARATOR]
    if len(arrows) != 1:
        raise UsageError(f"route must contain exactly one '{ROUTE_SEPARATOR}' separator")

    arrow = arrows[0]
    city_from = " ".join(route[:arrow]).strip()
    city_to = " ".join(route[arrow + 1 :]).strip()
    if not city_from or not city_to:
        raise UsageError("both cities must be specified")

    return ParsedRequest(
        city_from=city_from,
        city_to=city_to,
        trip_date=trip_date,
        time_from=time_from,
        time_to=time_to,
    )


def _parse_date(raw: str) -> date:
    try:
        return datetime.strptime(raw, DATE_FORMAT).date()
    except ValueError:
        raise UsageError("date must be in YYYY-MM-DD format") from None


def _parse_time(raw: str) -> time:
    try:
        return datetime.strptime(raw, "%H:%M").time()
    except ValueError:
        raise UsageError(f"invalid time '{raw}', expected HH:MM") from None
