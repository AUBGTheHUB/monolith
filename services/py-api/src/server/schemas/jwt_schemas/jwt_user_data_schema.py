from typing import TypedDict


class JwtUserData(TypedDict):
    sub: str
    is_admin: bool | None
    team_id: str | None
