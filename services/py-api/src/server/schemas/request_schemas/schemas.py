from typing import Literal, Optional, Union
from pydantic import EmailStr, BaseModel, Field, ConfigDict


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class BaseParticipantData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr


class AdminParticipantInputData(BaseParticipantData):
    registration_type: Literal["admin"]
    is_admin: Literal[True]
    team_name: str


class InviteLinkParticipantInputData(BaseParticipantData):
    registration_type: Literal["invite_link"]
    is_admin: Literal[False]
    team_name: str


class RandomParticipantInputData(BaseParticipantData):
    registration_type: Literal["random"]


class ParticipantRequestBody(BaseModel):
    registration_info: Union[AdminParticipantInputData, InviteLinkParticipantInputData, RandomParticipantInputData] = (
        Field(discriminator="registration_type")
    )


# TODO: Finish implementing the model below
class UpdateParticipantParams(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    email_verified: Optional[bool]
    is_admin: Optional[bool]
    team_name: Optional[str]
