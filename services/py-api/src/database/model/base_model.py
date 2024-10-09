from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, field_serializer


# https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers
class Base(BaseModel):
    _id: ObjectId
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @field_serializer("_id", check_fields=False)
    def serialize_dt(self, _id: ObjectId) -> str:
        return str(_id)
