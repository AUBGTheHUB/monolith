from dataclasses import dataclass
from typing import Annotated, Any

from bson import ObjectId
from pydantic import Field

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Group(BaseDbModel):
    """Represents a single matchup in a tournament bracket."""

    round: int
    bracket_number: Annotated[int, Field(ge=1, le=4)]

    first_team_id: ObjectId | None = None
    second_team_id: ObjectId | None = None
    winner_id: ObjectId | None = None

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "round": self.round,
            "bracket_number": self.bracket_number,
            "first_team_id": str(self.first_team_id) if self.first_team_id else None,
            "second_team_id": str(self.second_team_id) if self.second_team_id else None,
            "winner_id": str(self.winner_id) if self.winner_id else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "round": self.round,
            "bracket_number": self.bracket_number,
            "first_team_id": self.first_team_id,
            "second_team_id": self.second_team_id,
            "winner_id": self.winner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class GroupUpdateParams(UpdateParams):
    """Defines the fields that can be updated for a Group."""

    round: int | None = None
    bracket_number: Annotated[int, Field(ge=1, le=4)] | None = None

    first_team_id: ObjectId | None = None
    second_team_id: ObjectId | None = None
    winner_id: ObjectId | None = None
