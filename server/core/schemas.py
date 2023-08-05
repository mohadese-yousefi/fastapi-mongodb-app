from datetime import datetime, timezone
from typing import Any, Annotated, Union
from bson import ObjectId

from pydantic import BaseModel, Field, model_validator, ConfigDict, \
    PlainSerializer, AfterValidator, WithJsonSchema


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

class CreateModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = None

    @model_validator(mode='after')
    def updated_at_validator(self):
        self.updated_at = self.created_at
        return self 


class UpdateModel(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResponseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,)
    id: PyObjectId = Field(alias='_id')


class ExceptionModel(BaseModel):
    status_code: str
    detail: str
