import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from server.core.settings import settings


client = AsyncIOMotorClient(
    settings.MONGO_URI, serverSelectionTimeoutMS=10000
)
db = client.database


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except Exception as error:
            raise ValueError('Not a valid ObjectId') from error

    @classmethod
    def __modify_schema__(cls, field_schemas):
        field_schemas.update(type='string')
    
