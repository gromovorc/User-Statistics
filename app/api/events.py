from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse

from app.repositories.events_repo import InMemoryEventsRepo
from app.schemas.event import EventCreate, EventRead
from app.services.events_service import EventsService

events_router = APIRouter()

_repo = InMemoryEventsRepo()

def get_events_service() -> EventsService:
    return EventsService(repo=_repo)

@events_router.post(
    "/events"
)
def post_event(new_event: EventCreate
               , service: EventsService = Depends(get_events_service)
               ) -> JSONResponse:

    event, created = service.create_event(new_event)
    return JSONResponse(
        content=jsonable_encoder(event),
        status_code=201 if created else 200
    )