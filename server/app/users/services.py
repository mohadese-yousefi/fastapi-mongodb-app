import pathlib
from datetime import datetime
from os import fstat

from minio import Minio

from server.app.users.schemas import UserInput, User
from server.core.database import db
from server.core.schemas import PyObjectId
from server.core.settings import settings
from server.core.exceptions import FileExtentionNotValid

async def check_username(username: str, user_id: PyObjectId = None) -> bool:
    if user := await db['user'].find_one({'username': username}):
        if user.get('_id') != user_id:
            return False
    return True

async def create_user(user: UserInput) -> dict | None:
    if await check_username(username=user.username):
        user = User(**user.dict())
        new_user = await db['user'].insert_one(user.dict())
        created_user = await db['user'].find_one({'username': user.username})
        return created_user

def upload_file(file) -> dict:
    file_extention = pathlib.Path(file.filename).suffix
    if file_extention in settings.FILE_WHITE_LIST:
        object_name = f'{file.filename}.{datetime.now()}.{file_extention}'
        client = Minio(
                endpoint=settings.endpoint,
                access_key=settings.access_key,
                secret_key=settings.secret_key,
                secure=settings.MINIO_SECURE,
            ) 
        try:
            client.put_object(
                bucket_name=settings.bucket_name,
                object_name=object_name,
                data=file,
                length=fstat(file.fileno()).st_size,
            )
        except Exception as e:
            raise Exception(f"Error while trying to upload file. Exception: {e}")
    else:
        raise FileExtentionNotValid

    file_path = f'{settings.STORAGE_BASE_ENDPOINT}/{settings.bucket_name}/{object_name}'

    return {'file_path': file_path} 
