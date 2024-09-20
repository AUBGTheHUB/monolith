from pydantic import EmailStr, BaseModel


class ParticipantRequestBody(BaseModel):
    name: str
    email: EmailStr
    team_name: str
