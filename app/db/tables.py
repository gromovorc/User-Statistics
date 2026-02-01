from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Table, Column, Text, Integer, DateTime, MetaData, BigInteger

_metadata = MetaData()

events_table = Table(
    "events",
    _metadata,
    Column('id', BigInteger, primary_key=True),
    Column('event_id', UUID(as_uuid=True), nullable=False),
    Column('event_type', Text, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('event_time', DateTime(timezone=True), nullable=False),
    Column('ingested_at', DateTime(timezone=True), nullable=False),
    Column('properties', JSONB),
)