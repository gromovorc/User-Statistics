from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy as sa

from app.db.database import get_connection
from app.repositories.stats_repo_pg import PostgresStatsRepo
from app.schemas.stats import StatsResponse
from app.services.stats_service import StatsService

stats_router = APIRouter()

SessionDep = Annotated[sa.Connection, Depends(get_connection)]

def get_stats_repo(conn: SessionDep) -> PostgresStatsRepo:
    return PostgresStatsRepo(conn)

def get_stats_service(repo: PostgresStatsRepo=Depends(get_stats_repo)) -> StatsService:
    return StatsService(repo=repo)

@stats_router.get(
    "/users/{user_id}/stats",
    response_model=StatsResponse,
    status_code=200,
)
def get_stats(user_id:int,
              date_from: datetime | None = None,
              date_to: datetime | None = None,
              service: StatsService = Depends(get_stats_service)
              ):
    try:
        return service.get_user_stats(user_id=user_id, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))