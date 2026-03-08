import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db.models.events import events_table
from app.repositories.events_repo_interface import EventDict, AddResult


# noinspection PyTypeChecker
class PostgresEventsRepo:
    def __init__(self, conn: sa.Connection):
        self._unique_columns = ["user_id", "event_type", "event_time", "properties"]
        self._connection = conn

    def _is_same_payload(self, a: dict, b: dict) -> bool:
        return all(a[column] == b[column] for column in self._unique_columns)

    def add(self, event: EventDict) -> AddResult:
        insert_stmt = pg_insert(events_table).values(
            event_id = event["event_id"],
            event_time = event["event_time"],
            event_type = event["event_type"],
            user_id = event["user_id"],
            properties = event["properties"],
        ).on_conflict_do_nothing(index_elements=[events_table.c.event_id])

        with self._connection.begin():
            result = self._connection.execute(insert_stmt.returning(
                events_table.c.event_id,
                events_table.c.event_time,
                events_table.c.event_type,
                events_table.c.user_id,
                events_table.c.properties,
                events_table.c.ingested_at,
            ))

            inserted_row = result.mappings().first()

        if inserted_row:
            return dict(inserted_row), "created"

        select_stmt = sa.select(events_table).where(events_table.c.event_id == event["event_id"])
        existing = self._connection.execute(select_stmt).mappings().first()

        if existing and not self._is_same_payload(dict(existing), event):
            return dict(existing), "conflict"

        if existing:
            return dict(existing), 'duplicate'

    def list_user_events(self, user_id, date_from, date_to, limit, offset, event_type=None) -> list[dict]:
        select_stmt = sa.select(events_table).where(events_table.c.user_id == user_id)

        if date_from:
            select_stmt = select_stmt.where(events_table.c.event_time >= date_from)
        if date_to:
            select_stmt = select_stmt.where(events_table.c.event_time <= date_to)
        if event_type:
            select_stmt = select_stmt.where(events_table.c.event_type == event_type)

        select_stmt = select_stmt.order_by(events_table.c.event_time.desc()).limit(limit).offset(offset)

        rows = self._connection.execute(select_stmt).mappings().all()

        return [dict(row) for row in rows]