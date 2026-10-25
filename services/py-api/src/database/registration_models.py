from pydantic import BaseModel, EmailStr
from typing import Optional


class Participant(BaseModel):
    full_name: str
    age: int
    email: EmailStr
    university: str
    location: str
    share_info_with_sponsors: bool
    game_rank: str
    team_code: Optional[str] = None
    is_team_admin: bool = False


class Team(BaseModel):
    team_name: str
    team_code: str
    admin_email: EmailStr
    participant_count: int = 0
