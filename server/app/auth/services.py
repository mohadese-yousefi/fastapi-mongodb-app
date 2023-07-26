from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext
from jwt.exceptions import ExpiredSignatureError, PyJWKError, MissingRequiredClaimError
import jwt

from server.core.database import PyObjectId, db
from server.core.settings import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> dict | None:
    if user := await db['user'].find_one({'username': username}):
        if verify_password(password, user.get('password')):
            if user.get('active'):
                return user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Your account is not authorized',
            )


async def authenticate_token(user_id: str) -> dict | None:
    try:
        user_id = PyObjectId(user_id)
    except ValueError:
        return None
    if user := await db['user'].find_one({'_id': user_id}):
        if user.get('active'):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Your account is not authorized',
        )


async def generate_token(user_id: PyObjectId, role: str) -> dict:
    access = {
        'user_id': str(user_id),
        'role': str(role),
        'exp': datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    refresh = access.copy()
    refresh.update(
        {
            'exp': datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }
    )
    access_token = jwt.encode(access, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(
        refresh, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


async def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
    except (PyJWKError, ExpiredSignatureError, MissingRequiredClaimError):
        return None


async def auth_access(token: str, roles: list) -> dict | None:
    if payload := await decode_token(token):
        if payload.get('role') in roles:
            return payload.get('user_id')


async def auth_refresh(token: str) -> dict | None:
    if payload := await decode_token(token):
        if user := await authenticate_token(payload.get('user_id')):
            return await generate_token(
                user_id=user.get('_id'),
                password_ts=user.get('password_ts'),
            )