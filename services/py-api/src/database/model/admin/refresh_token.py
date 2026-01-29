from dataclasses import dataclass
from typing import Any
from src.database.model.base_model import BaseDbModel, SerializableObjectId, UpdateParams


@dataclass(kw_only=True)
class RefreshToken(BaseDbModel):
    hub_member_id: SerializableObjectId

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "hub_member_id": self.hub_member_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "hub_member_id": self.hub_member_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateRefreshTokenParams(UpdateParams):
    hub_member_id: str | None = None
