from typing import Dict, Any

from pydantic import BaseModel, field_serializer, ConfigDict

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team

# https://fastapi.tiangolo.com/tutorial/response-model/#response_model-parameter


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class ParticipantRegisteredInTeamResponse(BaseModel):
    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    model_config = ConfigDict(arbitrary_types_allowed=True)

    participant: Participant
    team: Team

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any]:
        return team.dump_as_json()
