from fastapi import APIRouter
from datetime import datetime

from app.schemas.event import EventCreate, EventRead
from app.services.events_service import EventsService

events_router = APIRouter()
events_service = EventsService()

@events_router.post(
    "/events",
    status_code=201
)
def post_event(new_event: EventCreate) -> EventRead:
    events_service.create_event(new_event)
    readed_event = EventRead(**new_event.model_dump(), ingested_at=datetime.now())

    return readed_event