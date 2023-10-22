from typing import List, Optional

from pydantic import BaseModel


class NewTeams(BaseModel):
    team_name: str
    team_members: List[str]


class UpdateTeam(BaseModel):
    team_name: Optional[str] = None
    team_members: Optional[List[str]] = None
