from server.app.users.schemas import UserInput, User
from server.core.database import PyObjectId, db

async def check_username(username: str, user_id: PyObjectId = None) -> bool:
    if user := await db['user'].find_one({'username': username}):
        if user.get('_id') != user_id:
            return False
    return True

async def create_user(user: UserInput) -> dict | None:
    if await check_username(username=user.username):
        user = User(**user.dict())
        new_user = await db['user'].insert_one(user.dict())
        created_user = await db['user'].find_one({'_id': new_user.inserted_id})
        return created_user
