from typing import Literal, Union
from pydantic import EmailStr, BaseModel, Field


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class AdminParticipantRequestBody(BaseModel):
    registration_type: Literal["admin"]
    is_admin: Literal[True]
    team_name: str


class InviteLinkParticipantRequestBody(BaseModel):
    registration_type: Literal["invite_link"]
    is_admin: Literal[False]
    team_name: str


class RandomParticipantRequestBody(BaseModel):
    registration_type: Literal["random"]


class ParticipantRequestBody(BaseModel):
    registration_info: Union[
        AdminParticipantRequestBody, InviteLinkParticipantRequestBody, RandomParticipantRequestBody
    ] = Field(discriminator="registration_type")
    name: str
    email: EmailStr
