from abc import ABC
from dataclasses import dataclass
from typing import Annotated

from bson import ObjectId
from pydantic import Field

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class Group(BaseDbModel, ABC):
    """Represents a single matchup in a tournament bracket."""

    round: int
    bracket_number: Annotated[int, Field(ge=1, le=4)]

    first_team_id: ObjectId | None = None
    second_team_id: ObjectId | None = None
    winner_id: ObjectId | None = None


class GroupUpdateParams(UpdateParams):
    """Defines the fields that can be updated for a Group."""

    round: int | None = None
    bracket_number: Annotated[int, Field(ge=1, le=4)] | None = None

    first_team_id: ObjectId | None = None
    second_team_id: ObjectId | None = None
    winner_id: ObjectId | None = None
