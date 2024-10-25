from typing import Dict, Any

from pydantic import BaseModel, field_serializer
from pydantic_core import to_jsonable_python

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class AdminParticipantRegisteredResponse(BaseModel):
    participant: Participant
    team: Team

    class Config:
        arbitrary_types_allowed = True

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any]:
        return team.dump_as_json()

    def json(self, *args, **kwargs) -> str:
        kwargs["default"] = to_jsonable_python  # Use Pydantic's encoder to handle ObjectId as str
        return super().json(*args, **kwargs)
