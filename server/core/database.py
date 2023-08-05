from motor.motor_asyncio import AsyncIOMotorClient

from server.core.settings import settings


client = AsyncIOMotorClient(
    settings.MONGO_URL, serverSelectionTimeoutMS=10000
)
db = client.database
