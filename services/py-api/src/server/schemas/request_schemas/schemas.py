from pydantic import EmailStr, BaseModel


# https://fastapi.tiangolo.com/tutorial/body/


class ParticipantRequestBody(BaseModel):
    name: str
    email: EmailStr
    team_name: str
    is_admin: bool
