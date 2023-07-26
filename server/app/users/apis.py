from fastapi import APIRouter, Depends, HTTPException, status

from server.app.users.schemas import (
    UserInput,
    UserOutput,
)
from server.app.users.services import (
    create_user,
)
from server.core.schemas import ExceptionModel


user_router = APIRouter(prefix='/users')

@user_router.post(
    '/',
    response_model=UserOutput,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {'model': ExceptionModel},
    },
    tags=['users'],
)
async def user_create(user: UserInput):
    if created_user := await create_user(user=user):
        return created_user

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'Username {user.username} already exists',
    )