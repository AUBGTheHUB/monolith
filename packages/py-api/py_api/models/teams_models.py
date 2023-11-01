from typing import List, Literal, Optional

from pydantic import BaseModel

TEAM_TYPE = Literal["normal", "random"]


class NewTeams(BaseModel):
    team_name: str
    team_members: List[str]
    team_type: TEAM_TYPE


class UpdateTeam(BaseModel):
    team_name: Optional[str] = None
    team_members: Optional[List[str]] = None
    team_type: Optional[TEAM_TYPE] = None
