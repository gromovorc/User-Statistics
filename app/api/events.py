from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, HTTPException
import sqlalchemy as sa

from app.db.database import get_connection
from app.db.tables import events_table
from app.repositories.events_repo_interface import EventsRepository
from app.repositories.events_repo_pg import PostgresEventsRepo
from app.schemas.event import EventCreate, EventRead
from app.services.events_service import EventsService

events_router = APIRouter()

SessionDep = Annotated[sa.Connection, Depends(get_connection)]

def get_events_repo(conn: SessionDep) -> EventsRepository:
    return PostgresEventsRepo(conn)

def get_events_service(repo: EventsRepository=Depends(get_events_repo)) -> EventsService:
    return EventsService(repo=repo)

@events_router.post(
    "/events",
    response_model=EventRead,
    status_code=201
)
def post_event(new_event: EventCreate,
               response: Response,
               service: EventsService = Depends(get_events_service)
               ):

    event, status = service.create_event(new_event)

    match status:
        case "created":
            response.status_code = 201
        case "duplicate":
            response.status_code = 200
        case "conflict":
            raise HTTPException(status_code=409, detail="The record conflicts with existing")
        case _:
            raise RuntimeError()

    return event

@events_router.get(
    "/users/{user_id}/events",
    response_model=list[EventRead],
    status_code=200,
)
def get_events(user_id:int,
              date_from: datetime | None = None,
              date_to: datetime | None = None,
              limit: int = 50,
              offset: int = 0,
              event_type: str | None = None,
              service: EventsService = Depends(get_events_service),
              ) -> list[EventRead]:
    try:
        return service.get_events(user_id=user_id,
                                  date_from=date_from,
                                  date_to=date_to,
                                  limit=limit,
                                  offset=offset,
                                  event_type=event_type)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
