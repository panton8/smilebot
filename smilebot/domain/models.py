from dataclasses import dataclass
from datetime import date, time

from smilebot.domain.statuses import RequestStatus


@dataclass(frozen=True, slots=True)
class SearchRequest:
    id: int
    chat_id: int
    city_from: str
    city_to: str
    trip_date: date
    time_from: time | None
    time_to: time | None
    status: RequestStatus

    def __post_init__(self) -> None:
        # psycopg maps TEXT columns to plain str; normalize to the enum.
        if not isinstance(self.status, RequestStatus):
            object.__setattr__(self, "status", RequestStatus(self.status))
