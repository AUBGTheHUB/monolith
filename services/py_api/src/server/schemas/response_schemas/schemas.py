from pydantic import BaseModel, EmailStr
from datetime import datetime


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class ParticipantResponse(BaseModel):
    # TODO: Add more fields once we know them or use the once from last year
    id: str
    name: str
    email: EmailStr
    email_verified: bool = False
    is_admin: bool
    created_at: datetime
    updated_at: datetime
