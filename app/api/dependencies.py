from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends

from app.db.database import get_connection
from app.repositories.events_repo_interface import EventsRepository
from app.repositories.events_repo_pg import PostgresEventsRepo
from app.repositories.stats_repo_pg import PostgresStatsRepo
from app.repositories.users_repo_interface import UsersRepository
from app.repositories.users_repo_pg import PostgresUsersRepo
from app.services.events_service import EventsService
from app.services.stats_service import StatsService
from app.services.users_service import UsersService

SessionDep = Annotated[sa.Connection, Depends(get_connection)]


def get_events_repo(conn: SessionDep) -> EventsRepository:
    return EventsRepository(conn)

def get_events_service(
    repo: EventsRepository = Depends(get_events_repo),
) -> EventsService:
    return EventsService(repo=repo)

def get_stats_repo(conn: SessionDep) -> PostgresStatsRepo:
    return PostgresStatsRepo(conn)

def get_stats_service(
    repo: PostgresStatsRepo = Depends(get_stats_repo),
) -> StatsService:
    return StatsService(repo=repo)

def get_users_repo(conn: SessionDep) -> PostgresUsersRepo:
    return PostgresUsersRepo(conn)

def get_users_service(
    repo: UsersRepository = Depends(get_users_repo),
) -> UsersService:
    return UsersService(repo=repo)