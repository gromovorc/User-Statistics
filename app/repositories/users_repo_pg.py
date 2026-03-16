import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db.models.users import users_table
from app.repositories.users_repo_interface import UserDict, UserCreateDict, UserAuthDict


# noinspection PyTypeChecker
class PostgresUsersRepo:
    def __init__(self, conn: sa.Connection):
        self._connection = conn

    def create(self, new_user: UserCreateDict) -> UserDict:
        insert_stmt = pg_insert(users_table).values(
            email = new_user["email"],
            username = new_user["username"],
            hashed_password = new_user["hashed_password"],
        )
        with self._connection.begin():
            result = self._connection.execute(insert_stmt.returning(
                users_table.c.id,
                users_table.c.email,
                users_table.c.username,
                users_table.c.created_at,
            ))
            inserted_row = result.mappings().first()

        return dict(inserted_row)

    def get_by_email(self, email: str) -> UserDict | None:
        select_stmt = sa.select(
            users_table.c.id,
            users_table.c.email,
            users_table.c.username,
            users_table.c.created_at
        ).where(users_table.c.email == email)
        result = self._connection.execute(select_stmt)
        user = result.mappings().first()

        return dict(user) if user else None

    def get_by_username(self, username: str) -> UserDict | None:
        select_stmt = sa.select(
            users_table.c.id,
            users_table.c.email,
            users_table.c.username,
            users_table.c.created_at
        ).where(users_table.c.username == username)
        result = self._connection.execute(select_stmt)
        user = result.mappings().first()

        return dict(user) if user else None

    def auth(self, login: str) -> UserAuthDict | None:

        select_stmt = sa.select(
            users_table.c.id,
            users_table.c.email,
            users_table.c.username,
            users_table.c.hashed_password
        ).where(
            sa.or_(
                users_table.c.email == login
                ,users_table.c.username == login
            )
        )
        result = self._connection.execute(select_stmt)
        user = result.mappings().first()
        return dict(user) if user else None

