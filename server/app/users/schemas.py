from datetime import datetime, timezone

from pydantic import BaseModel, root_validator
from enum import Enum

from server.app.auth.services import get_password_hash
from server.core.schemas import CreateModel, ResponseModel


class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class UserInput(BaseModel):
    username: str
    password: str
    email: str 
    first_name: str | None
    last_name: str | None


class User(CreateModel, UserInput):
    role: str = UserRole.USER.value
    active: bool = True

    @root_validator
    def password_validator(cls, values) -> dict:
        if password := values.get('password'):
            values['password'] = get_password_hash(password)
        return values

class UserOutput(ResponseModel):
    username: str
    email: str 
    first_name: str | None
    last_name: str | None
    role: str
    created_at: datetime

class UploaderOutput(BaseModel):
    file_path: str
