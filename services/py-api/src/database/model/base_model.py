from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import WithJsonSchema

from src.database.model.json_serializer import SerializableDbModel

SerializableObjectId = Annotated[ObjectId, WithJsonSchema({"type": "string", "format": "objectid"})]
"""As the original Mongo ObjectID is not json serializable this is needed to represent the ObjectID as a string in API
responses and OpenAPI documentation generated by FastAPI using the Pydantic Models. If we use the default one, the
Swagger page will throw an error because it cannot serialize the standard Mongo ObjectID
https://docs.pydantic.dev/latest/concepts/json_schema/#withjsonschema-annotation"""


# https://stackoverflow.com/questions/51575931/class-inheritance-in-python-3-7-dataclasses ans with 150 up votes
# https://www.trueblade.com/blogs/news/python-3-10-new-dataclass-features
@dataclass(kw_only=True)
class BaseDbModel(SerializableDbModel, ABC):
    id: SerializableObjectId = field(default_factory=ObjectId)
    """We create the ID on demand in order to use the created object as a return type of a function and have all the
    info as type safe attributes"""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class UpdateParams(BaseModel, ABC):
    updated_at: datetime = Field(default_factory=datetime.now)

    # Override the base class methods to exclude none by default, since we don't want the None values
    # to be present in the model dumps.

    # The base super().model_dump_json() returns a dict[str, Any], however mypy marks it as if it returns `Any`,
    # for this reason we are ignoring it.
    def model_dump(self, *, exclude_none: bool = True, **kwargs: dict[str, Any]) -> dict[str, Any]:
        return super().model_dump(exclude_none=exclude_none, **kwargs)  # type: ignore
