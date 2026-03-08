from datetime import datetime

import sqlalchemy as sa

from app.db.models.events import events_table


class PostgresStatsRepo:
    def __init__(self, conn: sa.Connection):
        self._connection = conn

    def total_events(self, user_id: int, date_from: datetime | None = None, date_to: datetime | None = None):
        select_stmt = (
            sa.select(sa.func.count(events_table.c.id).label("total"), sa.func.max(events_table.c.event_time).label("last_event_time"))
            .where(events_table.c.user_id == user_id)
                       )
        if date_from:
            select_stmt = select_stmt.where(events_table.c.event_time >= date_from)
        if date_to:
            select_stmt = select_stmt.where(events_table.c.event_time <= date_to)

        row = self._connection.execute(select_stmt).mappings().first()

        return row["total"], row["last_event_time"]

    def get_user_breakdown_by_type(self, user_id: int, date_from: datetime | None, date_to: datetime | None) -> dict[str, int]:
        select_stmt = (
            sa.select(events_table.c.event_type, sa.func.count(events_table.c.id).label("cnt"))
            .where(events_table.c.user_id == user_id)
            .group_by(events_table.c.event_type)
        )

        if date_from:
            select_stmt = select_stmt.where(events_table.c.event_time >= date_from)
        if date_to:
            select_stmt = select_stmt.where(events_table.c.event_time <= date_to)

        rows = self._connection.execute(select_stmt).mappings().all()
        
        return {row["event_type"]: row["cnt"] for row in rows}
