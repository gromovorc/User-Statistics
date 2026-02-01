from datetime import datetime, timezone
from typing import Dict, Tuple, Any, Literal

from app.repositories.events_repo_interface import EventDict, AddResult


class InMemoryEventsRepo:
    def __init__(self):
        self._events_by_id: Dict[str, EventDict] = {}
        self._unique_columns = ["user_id", "event_type", "event_time", "properties"]

    def _is_same_payload(self, a: dict, b: dict) -> bool:
        return all(a[column] == b[column] for column in self._unique_columns)

    def add(self, event: EventDict) -> AddResult:
        event_id = str(event["event_id"])
        existing = self._events_by_id.get(event_id)

        if existing and not self._is_same_payload(existing, event):
            return existing, "conflict"

        if existing:
            return existing, 'duplicate'

        self._events_by_id[event_id] = {**event, "ingested_at": datetime.now(timezone.utc)}
        return self._events_by_id[event_id], "created"
