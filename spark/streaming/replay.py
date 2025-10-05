from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import Iterable, Iterator


@dataclass(frozen=True)
class ReplayEvent:
    event_id: str
    source_row_reference: str
    occurred_at: datetime
    payload: dict


def timestamp_ordered(events: Iterable[ReplayEvent]) -> Iterator[ReplayEvent]:
    yield from sorted(events, key=lambda event: (event.occurred_at, event.event_id))


def replay(events: Iterable[ReplayEvent], speed: int = 10) -> Iterator[ReplayEvent]:
    if speed <= 0:
        raise ValueError("speed must be positive")
    previous: datetime | None = None
    for event in timestamp_ordered(events):
        if previous:
            sleep(max((event.occurred_at - previous).total_seconds() / speed, 0))
        previous = event.occurred_at
        yield event

