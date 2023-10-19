from typing import Optional

from pydantic import BaseModel


class NewTeams(BaseModel):
    team_name: str
    team_members: str


class UpdateTeam(BaseModel):
    team_name: Optional[str] = None
    team_members: Optional[str] = None
