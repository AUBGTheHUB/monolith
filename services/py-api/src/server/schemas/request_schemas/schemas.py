from typing import Optional
from pydantic import EmailStr, BaseModel, field_validator


# https://fastapi.tiangolo.com/tutorial/body/


class ParticipantRequestBody(BaseModel):
    name: str
    email: EmailStr
    team_name: Optional[str] = None
    is_admin: bool

    @field_validator("team_name", mode="before")
    @classmethod
    def check_team_name_when_admin(cls, team_name: Optional[str]) -> str:
        if slf.is_admin