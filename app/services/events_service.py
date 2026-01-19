from app.schemas.event import EventCreate

class EventsService:
    def __init__(self):
        self._events = list()

    def create_event(self, event: EventCreate) -> dict:
        self._events.append(event.model_dump())
        return self._events[-1]