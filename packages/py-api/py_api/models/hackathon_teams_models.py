from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel

# A "normal" team consists of the first participant (admin) who registered with a
# specific team_name and participants invited by the admin through a shareable link.

# A "random" team consists of participants who registered individually without
# specifying a team_name during registration.


class TeamType(str, Enum):
    NORMAL = "normal"
    RANDOM = "random"


class HackathonTeam(BaseModel):
    team_name: str
    team_members: List[str]
    team_type: TeamType
    is_verified: bool


class UpdateTeam(BaseModel):
    team_name: Optional[str] = None
    team_members: Optional[List[str]] = None
    is_verified: Optional[bool] = False


class MoveTeamMembers(BaseModel):
    from_team: str
    to_team: str
    team_members: List[str]
