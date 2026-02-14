from datetime import datetime

from app.repositories.stats_repo_pg import PostgresStatsRepo

from app.schemas.stats import StatsResponse


class StatsService:
    def __init__(self, repo: PostgresStatsRepo):
        self.repo = repo

    def get_user_stats(self, user_id: int, date_from: datetime | None, date_to: datetime | None) -> StatsResponse:
        if date_from and date_to and date_to < date_from:
            raise ValueError("Date to cannot be earlier than date from")

        total, last_time = self.repo.total_events(user_id, date_from, date_to)
        by_type = self.repo.get_user_breakdown_by_type(user_id, date_from, date_to)

        response = StatsResponse(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            total_events=total,
            by_type = by_type,
            last_event_time = last_time,
        )

        return response