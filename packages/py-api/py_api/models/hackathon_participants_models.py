from typing import Literal, Optional

from pydantic import BaseModel, EmailStr

TSHIRT_SIZE = Literal["S", "M", "L"]


class NewParticipant(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    tshirt_size: TSHIRT_SIZE
    team_name: Optional[str] = None
    is_verified: Optional[bool] = False
    is_admin: Optional[bool] = False


class UpdateParticipant(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    tshirt_size: Optional[TSHIRT_SIZE] = None
    team_name: Optional[str] = None
    is_verified: Optional[bool] = False
