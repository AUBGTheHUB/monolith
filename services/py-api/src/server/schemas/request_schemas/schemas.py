from typing import Literal, Union

from bson import ObjectId
from fastapi import HTTPException
from pydantic import EmailStr, BaseModel, Field, ConfigDict, field_validator


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class ResendEmailParticipantData(BaseModel):
    participant_id: str

    # https://docs.pydantic.dev/latest/concepts/validators/#field-validators
    @field_validator("participant_id", mode="before")
    @classmethod
    def validate_obj_id_format(cls, participant_id: str) -> str:
        if not ObjectId.is_valid(participant_id):
            raise HTTPException(detail="Wrong Object ID format", status_code=400)

        return participant_id


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
