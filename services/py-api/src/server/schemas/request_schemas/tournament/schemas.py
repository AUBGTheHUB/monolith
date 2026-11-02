from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TournamentParticipantReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=1, le=120)
    email: EmailStr
    university: str = Field(min_length=1, max_length=150)
    location: str = Field(min_length=1, max_length=150)
    share_info_with_sponsors: bool
    game_rank: str = Field(min_length=1, max_length=60)
    primary_role: str = Field(min_length=1, max_length=50)
    alternative_role: str = Field(min_length=1, max_length=50)


class TournamentAdminTeamReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    team_name: str = Field(min_length=2, max_length=80)
    tournament_participant: TournamentParticipantReqData


class TournamentParticipantJoinTeamReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    team_code: str = Field(min_length=6, max_length=32)
    tournament_participant: TournamentParticipantReqData
