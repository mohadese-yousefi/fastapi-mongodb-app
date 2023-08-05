from fastapi import APIRouter, Depends, HTTPException, status, \
    UploadFile, Form

from server.app.users.schemas import (
    UserInput,
    UserOutput,
    UploaderOutput,
)
from server.app.auth.schemas import TokenPayload
from server.app.auth.auth import get_current_user
from server.app.users.services import (
    create_user,
    upload_file,
)
from server.core.schemas import ExceptionModel


user_router = APIRouter(prefix='/users')

@user_router.post(
    '/',
    response_model=UserOutput,
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

@user_router.post(
    '/uploader',
    response_model=UploaderOutput,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ExceptionModel},
    },
)
def file_uploader(
    user: TokenPayload = Depends(get_current_user),
    file: UploadFile = Form(...)
    ):
    if file_path := upload_file(file):
        return file_path 

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'file is not support',
    )