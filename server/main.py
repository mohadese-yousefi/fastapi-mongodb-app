from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.core.routers import api_router
from server.core.settings import settings
from server.core.utils import CustomJSONResponse


app = FastAPI(title=settings.APP_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix='/api/v1')

@app.get('/')
def index():
    return CustomJSONResponse(200, 'message', 'Welcom to our site')
