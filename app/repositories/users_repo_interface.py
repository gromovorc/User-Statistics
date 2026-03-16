from datetime import datetime
from typing import Protocol, Any, TypedDict

class UserDict(TypedDict):
    id: int
    email: str
    username: str
    created_at: datetime

class UserCreateDict(TypedDict):
    email: str
    username: str
    hashed_password: str

class UserAuthDict(TypedDict):
    id: int
    email: str
    username: str
    hashed_password: str

class UsersRepository(Protocol):

    def create(self, user: UserCreateDict) -> UserDict:
        pass

    def get_by_email(self, email: str) -> UserDict | None:
        pass

    def get_by_username(self, username: str) -> UserDict | None:
        pass

    def auth(self, login: str) -> UserAuthDict | None:
        pass