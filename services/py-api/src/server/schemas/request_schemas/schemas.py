from typing import Literal, Union
from pydantic import EmailStr, BaseModel


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class ParticipantBaseRequestBody(BaseModel):
    name: str
    email: EmailStr


class AdminParticipantRequestBody(ParticipantBaseRequestBody):
    type: Literal["admin"]
    is_admin: Literal[True]
    team_name: str


class InviteLinkParticipantRequestBody(ParticipantBaseRequestBody):
    type: Literal["invite_link"]
    is_admin: Literal[False]
    team_name: str


class RandomParticipantRequestBody(ParticipantBaseRequestBody):
    type: Literal["random"]


ParticipantRequestBody = Union[
    AdminParticipantRequestBody,
    RandomParticipantRequestBody,
    InviteLinkParticipantRequestBody,
]
