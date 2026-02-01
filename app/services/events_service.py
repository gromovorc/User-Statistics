from app.repositories.events_repo_interface import EventsRepository
from app.schemas.event import EventCreate
from typing import Dict, Tuple, Any, Literal


class EventsService:
    def __init__(self, repo: EventsRepository):
        self.repo = repo

    def create_event(self, event: EventCreate) -> Tuple[Dict[str, Any], Literal["created", "duplicate", "conflict"]]:
        new_event = event.model_dump()
        return self.repo.add(new_event)