from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_users_service
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead, UserAuth
from app.services.users_service import UsersService

router = APIRouter(tags=["auth"])


@router.post(
    "/auth/register",
    response_model=UserRead,
    status_code=201,
)
def register_user(
    new_user: UserCreate,
    service: UsersService = Depends(get_users_service),
):
    try:
        return service.register_user(new_user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/auth/login")
async def login_for_access_token(
    auth_user: UserAuth,
    service: UsersService = Depends(get_users_service),
) -> Token:
    try:
        user = service.auth_user(auth_user)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user["id"])}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
