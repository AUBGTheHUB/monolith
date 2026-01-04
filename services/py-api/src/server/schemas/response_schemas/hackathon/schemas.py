"""Here we store schemas modeling how the response of a given request should look like. These schemas are also used
by FastAPI for swagger docs.

We use the term "schema" as it is in accordance with the OpenAPI spec:
https://swagger.io/docs/specification/v3_0/data-models/data-models/"""

from typing import Any, Optional

from pydantic import BaseModel, field_serializer, ConfigDict

from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse


class ParticipantResponse(BaseModel):
    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    model_config = ConfigDict(arbitrary_types_allowed=True)

    participant: Participant

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> dict[str, Any]:
        return participant.dump_as_json()


class ParticipantAndTeamResponse(ParticipantResponse):
    team: Optional[Team]

    @field_serializer("team")
    def serialize_team(self, team: Team) -> dict[str, Any] | None:
        if team:
            return team.dump_as_json()

        return None


class TeamResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    team: Team

    @field_serializer("team")
    def serialize_team(self, team: Team) -> dict[str, Any] | None:
        return team.dump_as_json()


class AllTeamsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    teams: list[Team]

    @field_serializer("teams")
    def serialize_teams(self, teams: list[Team]) -> list[dict[str, Any]]:
        return [team.dump_as_json() for team in teams]


class ParticipantRegisteredResponse(ParticipantAndTeamResponse):
    """
    Responds with the registred documents of the Participant and Team. The Team object is only
    returned when we are registering an admin participant
    """


class ParticipantDeletedResponse(ParticipantResponse):
    """
    Responds with the deleted participant body when we are deleting a participant.
    """


class ParticipantVerifiedResponse(ParticipantAndTeamResponse):
    """This response includes the updated body of the verified participant
    and the body of the verified team in case we are verifying an admin participant.
    """


class VerificationEmailSentSuccessfullyResponse(ParticipantResponse):
    """This response includes the updated body of the participant
    after successfully resending a verification email
    """


class TeamDeletedResponse(TeamResponse):
    """
    Responds with the deleted team body when we are deleting a team.
    """


class RegistrationClosedSuccessfullyResponse(FeatureSwitchResponse):
    """
    Response sent when the endpoint for closing the application is triggered.
    """
