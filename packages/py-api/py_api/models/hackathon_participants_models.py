from typing import Literal, Optional

from pydantic import BaseModel

TSHIRT_SIZE = Literal["S", "M", "L"]


class NewParticipant(BaseModel):
    first_name: str
    last_name: str
    email: str
    tshirt_size: TSHIRT_SIZE


class UpdateParticipant(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    tshirt_size: Optional[TSHIRT_SIZE] = None
