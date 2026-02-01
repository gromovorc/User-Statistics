"""create events table

Revision ID: a2b9c1e96dfa
Revises: 
Create Date: 2026-01-31 22:55:21.138228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a2b9c1e96dfa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'events',
        sa.Column('id', postgresql.BIGINT, sa.Identity(), nullable=False),
        sa.Column('event_id', postgresql.UUID(as_uuid=True),nullable=False),
        sa.Column('event_type', postgresql.VARCHAR, nullable=False),
        sa.Column('user_id', postgresql.INTEGER, nullable=False),
        sa.Column('event_time', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('ingested_at', postgresql.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
        sa.Column('properties', postgresql.JSONB, nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id'),
    )

    op.create_index('ix1_events', 'events', ['user_id', 'event_time'])
    op.create_index('ix2_events', 'events', ['event_type', 'event_time'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_events_user_time', table_name='events')
    op.drop_index('ix_events_type_time', table_name='events')
    op.drop_table('events')
