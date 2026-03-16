from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_stats_service
from app.schemas.stats import StatsResponse
from app.services.stats_service import StatsService

router = APIRouter(tags=["stats"])


@router.get(
    "/users/{user_id}/stats",
    response_model=StatsResponse,
    status_code=200,
)
def get_stats(
    user_id: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    service: StatsService = Depends(get_stats_service),
):
    try:
        return service.get_user_stats(user_id=user_id, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))