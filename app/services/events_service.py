from app.schemas.event import EventCreate
from typing import Dict, Tuple, Any


class EventsService:
    def __init__(self, repo):
        self.repo = repo

    def create_event(self, event: EventCreate) -> Tuple[Dict[str, Any], bool]:
        new_event = event.model_dump()
        return self.repo.add(new_event)