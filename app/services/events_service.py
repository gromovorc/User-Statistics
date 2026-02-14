from datetime import datetime

from app.repositories.events_repo_interface import EventsRepository
from app.schemas.event import EventCreate
from typing import Dict, Tuple, Any, Literal


class EventsService:
    def __init__(self, repo: EventsRepository):
        self.repo = repo

    def create_event(self, event: EventCreate) -> Tuple[Dict[str, Any], Literal["created", "duplicate", "conflict"]]:
        new_event = event.model_dump()
        return self.repo.add(new_event)

    def get_events(self,
                       user_id: int,
                       date_from: datetime | None,
                       date_to: datetime | None,
                       limit: int,
                       offset: int,
                       event_type: str |  None) -> list[dict]:

        if date_from and date_to and date_to < date_from:
            raise ValueError("Date to cannot be earlier than date from")

        if not 1 <= limit <= 100:
            raise ValueError("Limit out of acceptable range")

        if offset < 0:
            raise ValueError("Negative offset")

        return self.repo.list_user_events(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
            event_type=event_type,
        )
