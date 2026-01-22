from datetime import datetime, timezone
from typing import Dict, Tuple, Any


class InMemoryEventsRepo:
    def __init__(self):
        self._events_by_id: Dict[str, Dict[str, Any]] = {}

    def add(self, event: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        event_id = str(event["event_id"])
        existing = self._events_by_id.get(event_id)

        if existing:
            return existing, False

        self._events_by_id[event_id] = {**event, "ingested_at": datetime.now(timezone.utc)}
        return event, True
