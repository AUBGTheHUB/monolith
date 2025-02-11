from typing import Any, Literal, Optional, Union
from fastapi.types import IncEx
from pydantic import EmailStr, BaseModel, Field, ConfigDict
from src.database.model.participant_model import (
    ALLOWED_AGE,
    PROGRAMMING_LANGUAGES_LIST,
    PROGRAMMING_LEVELS_LIST,
    REFERRAL_SOURCES_LIST,
    TSHIRT_SIZE,
    UNIVERSITIES_LIST,
)


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class ResendEmailParticipantData(BaseModel):
    participant_id: str


class BaseParticipantData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr
    tshirt_size: Optional[TSHIRT_SIZE] = None
    university: UNIVERSITIES_LIST
    location: str
    age: ALLOWED_AGE
    source_of_referral: Optional[REFERRAL_SOURCES_LIST] = None
    programming_language: Optional[PROGRAMMING_LANGUAGES_LIST] = None
    programming_level: Optional[PROGRAMMING_LEVELS_LIST] = None
    has_participated_in_hackaubg: bool
    has_internship_interest: bool
    has_participated_in_hackathons: bool
    has_previous_coding_experience: bool
    share_info_with_sponsors: bool

    # We need to use the dump of the input data to pass it to the repository layer, however `registration_type` and `team_name` are not
    # part of the participant document, thus we shall exclude them from the dump.
    # `registration_type` only helps us to determine the registration manner in a more elegant way.
    # `team_name` helps us with determining the name of the team that the admin participant wants to create
    def model_dump(
        self, *, exclude: IncEx = ["registration_type", "team_name"], **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        return super().model_dump(exclude=exclude, **kwargs)  # type: ignore


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
