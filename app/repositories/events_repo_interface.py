from typing import Protocol, Any, Literal

EventDict = dict[str, Any]
AddStatus = Literal["created", "duplicate", "conflict"]
AddResult = tuple[EventDict, AddStatus]

class EventsRepository(Protocol):

    def add(self, event: EventDict) -> AddResult:
        pass

    def list_user_events(self, *args, **kwargs) -> list[EventDict]:
        pass