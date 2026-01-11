from typing import Mapping, Any

from pydantic import BaseModel, ConfigDict, field_serializer
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from src.database.model.feature_switch_model import FeatureSwitch


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
        self.response_model = response_model


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class FeatureSwitchResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    feature: FeatureSwitch

    @field_serializer("feature")
    def serialize_feature(self, feature: FeatureSwitch) -> dict[str, Any]:
        return feature.dump_as_json()


class AllFeatureSwitchesResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    features: list[FeatureSwitch]

    @field_serializer("features")
    def serialize_features(self, features: list[FeatureSwitch]) -> list[dict[str, Any]]:
        return [feature.dump_as_json() for feature in features]


class ParticipantResponse(BaseModel):
    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    model_config = ConfigDict(arbitrary_types_allowed=True)

    participant: Participant

    @field_serializer("participant")
    def serialize_participant(self, participant: Participant) -> Dict[str, Any]:
        return participant.dump_as_json()


class ParticipantAndTeamResponse(ParticipantResponse):
    team: Optional[Team]

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any] | None:
        if team:
            return team.dump_as_json()

        return None


class TeamResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    team: Team

    @field_serializer("team")
    def serialize_team(self, team: Team) -> Dict[str, Any] | None:
        return team.dump_as_json()


class AllTeamsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    teams: List[Team]

    @field_serializer("teams")
    def serialize_teams(self, teams: List[Team]) -> List[Dict[str, Any]]:
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


class AdminTeamMemberOut(BaseModel):
    name: str
    photo_url: str
    linkedin_url: str


class AdminDepartmentOut(BaseModel):
    id: str
    name: str
    members: List[AdminTeamMemberOut]


class AdminDepartmentsListOut(BaseModel):
    departments: List[AdminDepartmentOut]
