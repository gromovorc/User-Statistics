from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length = 3)
    password: str = Field(..., min_length = 6)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserAuth(BaseModel):
    login: str
    password: str = Field(..., min_length=6)