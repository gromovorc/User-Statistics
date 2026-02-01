from datetime import datetime, timedelta, timezone

from typing import Any
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator

class EventCreate(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_time: datetime
    event_type: str = Field(..., min_length = 1)
    user_id: int = Field(..., gt=0)
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator('event_time')
    def validate_time(cls, time_given: datetime):
        utc_timezone = timezone.utc
        time_given = time_given.astimezone(utc_timezone)
        now_utc = datetime.now(utc_timezone)

        if time_given - now_utc > timedelta(minutes=10):
            raise ValueError("The time too far in the future")

        return time_given


class EventRead(EventCreate):
    ingested_at: datetime