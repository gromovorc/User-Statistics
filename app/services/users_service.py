from app.core.security import get_password_hash

from app.repositories.users_repo_interface import UsersRepository, UserDict, UserCreateDict
from app.schemas.user import UserCreate, UserAuth


class UsersService:
    def __init__(self, repo: UsersRepository):
        self._repo = repo

    def create_user(self, user: UserCreate) -> UserDict:
        new_user = user.model_dump()
        return self._repo.create(new_user)

    def register_user(self, user: UserCreate) -> UserDict:
        if self._repo.get_by_email(user.email):
            raise ValueError("Email already exists")
        if self._repo.get_by_username(user.username):
            raise ValueError("Username taken")
        new_user: UserCreateDict = {
            "email": user.email,
            "username": user.username,
            "hashed_password": get_password_hash(user.password)
        }

        return self._repo.create(new_user)

    def auth_user(self, user: UserAuth) -> UserDict:
        db_user = self._repo.auth(user.login)
        if not db_user:
            raise ValueError("Invalid credentials")
        if not get_password_hash(db_user.password) == db_user.password:
            raise ValueError("Invalid credentials")

        return {
            "id": db_user["id"],
            "email": db_user["email"],
            "username": db_user["username"],
        }
