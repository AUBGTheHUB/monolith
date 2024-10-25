from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from src.database.model.json_serializer import Serializer


# https://stackoverflow.com/questions/51575931/class-inheritance-in-python-3-7-dataclasses ans with 150 up votes
# https://www.trueblade.com/blogs/news/python-3-10-new-dataclass-features
@dataclass(kw_only=True)
class Base(Serializer, ABC):
    _id: ObjectId = field(default_factory=lambda: ObjectId())
    """This is with underscore as MongoDB expects it like this. We create the ID on demand in order to return the whole
    object and have type safe attributes when used as a return type of a function"""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def id(self) -> ObjectId:
        return self._id

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema):
        return {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "is_admin": {"type": "boolean"},
                "email_verified": {"type": "boolean"},
                "team_id": {"type": "string"},  # Handle ObjectId as string
            },
            "required": ["name", "email", "is_admin"],
        }

    @classmethod
    def __get_pydantic_core_schema__(cls, _schema):
        return cls.__get_pydantic_json_schema__(_schema)
