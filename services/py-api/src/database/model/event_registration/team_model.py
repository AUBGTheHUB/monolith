from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.database.model.base_model import (
    BaseDbModel,
    SerializableObjectId,
)


@dataclass(kw_only=True)
class Team(BaseDbModel):
    """Team registered for the separate Project S event."""

    name: str
    code: str
    leader_id: SerializableObjectId

    member_count: int = field(default=1)
    completed_at: datetime | None = None
    completion_email_sent_at: datetime | None = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "code": self.code,
            "leader_id": self.leader_id,
            "member_count": self.member_count,
            "completed_at": self.completed_at,
            "completion_email_sent_at": self.completion_email_sent_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "leader_id": str(self.leader_id),
            "member_count": self.member_count,
            "completed_at": (self.completed_at.isoformat() if self.completed_at else None),
            "completion_email_sent_at": (
                self.completion_email_sent_at.isoformat() if self.completion_email_sent_at else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
