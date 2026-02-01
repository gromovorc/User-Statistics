from typing import Protocol
from typing import Any, Literal

EventDict = dict[str, Any]
AddStatus = Literal["created", "duplicate", "conflict"]
AddResult = tuple[EventDict, AddStatus]

class EventsRepository(Protocol):

    def add(self, event: EventDict) -> AddResult:
        ...