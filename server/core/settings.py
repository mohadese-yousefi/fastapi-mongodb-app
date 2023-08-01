import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_TITLE : str = os.environ.get('PROJECT_NAME', 'My Fast API')
    TIME_ZONE : str = 'UTC'
    STORAGE_BASE_ENDPOINT: str = os.environ.get('STORAGE_BASE_ENDPOINT', '127.0.0.1:9000')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2 # 2 days 
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = 'HS256' #RSASSA-PKCS1-v1_5 using SHA-256
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', 'template')   # should be kept secret
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://flask:flaskpass@127.0.0.1:27017/fastdb?authSource=admin')
    FILE_WHITE_LIST: list = ['png', 'pdf', 'jpg', 'jpeg', 'svg']

    MINIO_ROOT_USER = os.environ.get('MINIO_ROOT_USER', 'username')
    MINIO_ROOT_PASSWORD = os.environ.get('MINIO_ROOT_PASSWORD', 'password')
    MINIO_HOST = os.environ.get('MINIO_HOST', 'localhost')
    MINIO_PORT = os.environ.get('MINIO_PORT', '9000')
    MINIO_SECURE: bool = os.environ.get('MINIO_SECURE', 'False')
    MINIO_BUCKET_NAME = os.environ.get('MINIO_BUCKET_NAME', 'my-bucket')
    MINIO_URI = os.environ.get('MINIO_URL', 'localhost')

@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
