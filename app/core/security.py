from datetime import timedelta, timezone, datetime

import jwt
from pwdlib import PasswordHash

from app.core.config import SECRET_KEY, ALGORITHM

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# def authenticate_user(username: str, password: str):
#     user = user_repo.get_by_username(username=username)
#     if not user:
#         user = user_repo.get_by_email(email=username)
#         verify_password(password)
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt