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

def get_repo(conn: SessionDep) -> EventsRepository:
    return PostgresEventsRepo(conn)

def get_service(repo: EventsRepository=Depends(get_repo)) -> EventsService:
    return EventsService(repo=repo)

@events_router.post(
    "/events",
    response_model=EventRead,
    status_code=201
)
def post_event(new_event: EventCreate,
               response: Response,
               service: EventsService = Depends(get_service)
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


############################################



@events_router.get(
    "/debug/db",
    status_code=200
)
def get_event_by_id(conn: SessionDep, event_id:UUID):

    query1 = sa.select(events_table).where(events_table.c.event_id == event_id)
    result = conn.execute(query1)

    row = result.mappings().first()

    return dict(row) if row else {"found": False}

