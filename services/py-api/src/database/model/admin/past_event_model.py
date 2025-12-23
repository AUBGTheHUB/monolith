from dataclasses import dataclass, field
from typing import Any

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class PastEvent(BaseDbModel):
    title: str
    cover_picture: str
    tags: list[str] = field(default_factory=list)

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "title": self.title,
            "cover_picture": self.cover_picture,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "title": self.title,
            "cover_picture": self.cover_picture,
            "tags": self.tags,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdatePastEventParams(UpdateParams):
    title: str | None = None
    cover_picture: str | None = None
    tags: list[str] | None = None
