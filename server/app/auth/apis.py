from fastapi import APIRouter, HTTPException, status

from server.app.auth.schemas import Credentials, Refresh, Token
from server.app.auth.services import auth_refresh, authenticate_user, \
    generate_token
from server.core.schemas import ExceptionModel


auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post(
    '/token', 
    response_model=Token, 
    responses={401: {'model': ExceptionModel}}
)
async def token(credentials: Credentials):
    if user := await authenticate_user(
        username=credentials.username, password=credentials.password
    ):
        return await generate_token(
            user_id=user.get('_id'),
            role=user.get('role'),
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@auth_router.post(
    '/refresh',
    response_model=Token,
    responses={401: {'model': ExceptionModel}}
)
async def refresh(payload: Refresh):
    if new_token := await auth_refresh(token=payload.refresh_token):
        return new_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired token',
        headers={'WWW-Authenticate': 'Bearer'},
    )
