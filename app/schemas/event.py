from datetime import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_time: datetime
    event_type: str = Field(..., min_length = 1)
    user_id: int = Field(..., gt=0)
    properties: dict = Field(default_factory=dict)

class EventRead(EventCreate):
    ingested_at: datetime