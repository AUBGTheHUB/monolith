from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ParticipantInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    full_name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=1, le=120)
    email: EmailStr
    university: str = Field(min_length=1, max_length=150)
    location: str = Field(min_length=1, max_length=150)
    share_info_with_sponsors: bool
    game_rank: str = Field(min_length=1, max_length=60)
    primary_role: str = Field(min_length=1, max_length=50)
    alternative_role: str = Field(min_length=1, max_length=50)


class CreateTeamRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    team_name: str = Field(min_length=2, max_length=80)
    participant: ParticipantInput


class JoinTeamRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    team_code: str = Field(min_length=6, max_length=32)
    participant: ParticipantInput


class SoloRegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    participant: ParticipantInput


class AssignSoloMemberRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    participant_id: str = Field(min_length=24, max_length=24)
    team_code: str = Field(min_length=6, max_length=32)
    assigned_role: str = Field(min_length=1, max_length=50)
