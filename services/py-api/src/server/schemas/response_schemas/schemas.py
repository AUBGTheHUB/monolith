from typing import Dict, Any, Optional, Mapping

from pydantic import BaseModel, field_serializer, ConfigDict
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


class Response(JSONResponse):
    """A thin wrapper over the Starlette JSONResponse class. This wrapper allows us to pass Response models, which are
    automatically serialized to JSON under the hood.

    For more info: https://fastapi.tiangolo.com/tutorial/response-model/
    """

    def __init__(
        self,
        response_model: BaseModel,
        status_code: int,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(
            content=response_model.model_dump(),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class ParticipantRegisteredResponse(BaseModel):
    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    model_config = ConfigDict(arbitrary_types_allowed=True)

    participant: Participant
    team: Optional[Team]

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any] | None:
        if team:
            return team.dump_as_json()

        return None


class ParticipantDeletedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    participant: Participant

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()


class TeamDeletedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    team: Team

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any] | None:
        return team.dump_as_json()
