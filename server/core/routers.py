from fastapi import APIRouter

from server.app.auth.apis import auth_router
from server.app.users.apis import user_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
