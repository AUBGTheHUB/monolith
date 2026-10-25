from dataclasses import dataclass
from typing import Any

from src.database.model.base_model import (
    BaseDbModel,
    SerializableObjectId,
)


@dataclass(kw_only=True)
class Participant(BaseDbModel):
    """Participant registered for the separate Project S event."""

    full_name: str
    age: int
    email: str
    university: str
    location: str
    share_info_with_sponsors: bool
    game_rank: str
    primary_role: str
    alternative_role: str

    team_id: SerializableObjectId | None = None
    is_team_leader: bool = False
    assigned_role: str | None = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "full_name": self.full_name,
            "age": self.age,
            "email": self.email,
            "university": self.university,
            "location": self.location,
            "share_info_with_sponsors": self.share_info_with_sponsors,
            "game_rank": self.game_rank,
            "primary_role": self.primary_role,
            "alternative_role": self.alternative_role,
            "team_id": self.team_id,
            "is_team_leader": self.is_team_leader,
            "assigned_role": self.assigned_role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "age": self.age,
            "email": self.email,
            "university": self.university,
            "location": self.location,
            "share_info_with_sponsors": self.share_info_with_sponsors,
            "game_rank": self.game_rank,
            "primary_role": self.primary_role,
            "alternative_role": self.alternative_role,
            "team_id": str(self.team_id) if self.team_id else None,
            "is_team_leader": self.is_team_leader,
            "assigned_role": self.assigned_role,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
