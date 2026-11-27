from enum import StrEnum


class RequestStatus(StrEnum):
    ACTIVE = "active"
    FOUND = "found"
    CLOSED = "closed"
    EXPIRED = "expired"


ALLOWED_TRANSITIONS: dict[RequestStatus, frozenset[RequestStatus]] = {
    RequestStatus.ACTIVE: frozenset(
        {RequestStatus.FOUND, RequestStatus.CLOSED, RequestStatus.EXPIRED}
    ),
    RequestStatus.FOUND: frozenset({RequestStatus.CLOSED, RequestStatus.EXPIRED}),
    RequestStatus.CLOSED: frozenset(),
    RequestStatus.EXPIRED: frozenset(),
}


def can_transition(current: RequestStatus, target: RequestStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
