from datetime import datetime, timedelta, timezone

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt.exceptions import ExpiredSignatureError, PyJWKError, MissingRequiredClaimError
import jwt
from server.app.auth.exception import NotAuthorizedException

from server.core.schemas import PyObjectId
from server.app.auth.schemas import TokenPayload
from server.core.database import db
from server.core.settings import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl='user_token',
    scheme_name='JWT',
)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> dict | None:
    if user := await db['user'].find_one({'username': username}):
        if await verify_password(password, user.get('password')):
            if user.get('active'):
                return user

    raise NotAuthorizedException


async def authenticate_token(user_id: str) -> dict:
    try:
        user_id = PyObjectId(user_id)
    except ValueError:
        return None
    if user := await db['user'].find_one({'_id': user_id}):
        if user.get('active'):
            return user
        raise NotAuthorizedException


async def generate_access_token(user_id: str, role: str) -> str:
    access = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(
        access, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return access_token


async def generate_refresh_token(user_id: str, role: str) -> str:
    refresh = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    refresh_token = jwt.encode(
        refresh, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return refresh_token


async def generate_token(user_id: PyObjectId, role: str) -> dict:
    access_token = await generate_access_token(str(user_id), role)
    refresh_token = await generate_refresh_token(str(user_id), role)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


async def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=settings.ALGORITHM,
        )
    except (PyJWKError, ExpiredSignatureError, MissingRequiredClaimError):
        raise NotAuthorizedException


async def auth_refresh(token: str) -> dict | None:
    if payload := await decode_token(token):
        if user := await authenticate_token(payload.get('user_id')):
            return await generate_token(
                user_id=user.get('_id'),
                password_ts=user.get('password_ts'),
            )


async def get_current_user(
        token: str = Depends(reuseable_oauth)) -> TokenPayload:
    token_data = await decode_token(token)

    if datetime.fromtimestamp(token_data.exp) < datetime.now():
        raise NotAuthorizedException

    return TokenPayload(**token_data)
