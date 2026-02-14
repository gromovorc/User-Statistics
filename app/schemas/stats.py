from datetime import datetime

from pydantic import BaseModel, Field

class StatsResponse(BaseModel):
    user_id: int
    date_from: datetime | None
    date_to: datetime | None
    total_events: int = 0
    by_type: dict[str, int] = Field(default_factory=dict)
    last_event_time: datetime | None