from sqlalchemy import Table, Column, Text, DateTime, BigInteger, func, UniqueConstraint, String

from app.db.database import metadata

users_table = Table(
    "users",
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('email', String(255), nullable=False),
    Column('username', String(100), nullable=False),
    Column('hashed_password', Text, nullable=False),

    Column(
        'created_at',
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    ),
    Column(
        'updated_at',
           DateTime(timezone=True),
           nullable=False,
           server_default=func.now(),
           onupdate=func.now()
    ),

    UniqueConstraint("username", name="uix_users_username"),
    UniqueConstraint("email", name="uix_users_email"),
)