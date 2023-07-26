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
    MONGO_URI: str = os.environ.get('MONGO_URL', 'mongodb://flask:flaskpass@127.0.0.1:27017/fastdb?authSource=admin')

@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
