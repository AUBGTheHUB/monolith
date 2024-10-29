from typing import Dict, Any

from pydantic import BaseModel, field_serializer

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class ParticipantRegisteredInTeamResponse(BaseModel):
    participant: Participant
    team: Team

    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    class Config:
        arbitrary_types_allowed = True

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any]:
        return team.dump_as_json()
