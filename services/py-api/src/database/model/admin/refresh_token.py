from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union
from src.database.model.base_model import BaseDbModel, SerializableObjectId, UpdateParams


@dataclass(kw_only=True)
class RefreshToken(BaseDbModel):
    hub_member_id: SerializableObjectId
    family_id: str
    expires_at: datetime
    is_valid: bool

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "is_valid": self.is_valid,
            "family_id": self.family_id,
            "hub_member_id": self.hub_member_id,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "hub_member_id": self.hub_member_id,
            "is_valid": self.is_valid,
            "family_id": self.family_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": self.expires_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateRefreshTokenParams(UpdateParams):
    hub_member_id: str | None = None
    is_valid: Union[bool, None] = None
