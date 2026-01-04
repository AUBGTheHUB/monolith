"""Here we store schemas modeling how the request body of a given request should look like. These schemas are also used
by FastAPI for swagger docs.

We use the term "schema" as it is in accordance with the OpenAPI spec:
https://swagger.io/docs/specification/v3_0/data-models/data-models/"""

from typing import Any, Literal, Optional, Union

from fastapi.types import IncEx
from pydantic import EmailStr, BaseModel, Field, ConfigDict, field_validator

from src.database.model.hackathon.participant_model import (
    ALLOWED_AGE,
    PROGRAMMING_LANGUAGES_LIST,
    PROGRAMMING_LEVELS_LIST,
    REFERRAL_SOURCES_LIST,
    TSHIRT_SIZE,
    UNIVERSITIES_LIST,
)
from src.server.schemas.request_schemas.schemas import NonEmptyStr


# https://fastapi.tiangolo.com/tutorial/body/
# https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions


class BaseParticipantData(BaseModel):
    # Forbid extra fields
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr = Field(max_length=50, min_length=3)
    email: EmailStr = Field(max_length=320, min_length=3)
    tshirt_size: Optional[TSHIRT_SIZE] = None
    university: UNIVERSITIES_LIST
    location: NonEmptyStr = Field(max_length=100, min_length=3)
    age: ALLOWED_AGE
    source_of_referral: Optional[REFERRAL_SOURCES_LIST] = None
    programming_language: Optional[PROGRAMMING_LANGUAGES_LIST] = None
    programming_level: Optional[PROGRAMMING_LEVELS_LIST] = None
    has_participated_in_hackaubg: bool
    has_internship_interest: bool
    has_participated_in_hackathons: bool
    has_previous_coding_experience: bool
    share_info_with_sponsors: bool

    @field_validator("share_info_with_sponsors", mode="before")
    @classmethod
    def check_if_true(cls, value: bool) -> bool:
        if not value:
            raise ValueError("share_info_with_sponsors shall be true")
        return value

    # We need to use the dump of the input data to pass it to the repository layer, however `registration_type` and
    # `team_name` are not part of the participant document, thus we shall exclude them from the dump.

    # `registration_type` only helps us to determine the registration manner in a more elegant way.
    # `team_name` helps us with determining the name of the team that the admin participant wants to create
    def model_dump(
        self, *, exclude: IncEx = ("registration_type", "team_name"), **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        return super().model_dump(exclude=exclude, **kwargs)  # type: ignore


class AdminParticipantInputData(BaseParticipantData):
    registration_type: Literal["admin"]
    is_admin: Literal[True]
    team_name: NonEmptyStr = Field(max_length=30, min_length=1)


class InviteLinkParticipantInputData(BaseParticipantData):
    registration_type: Literal["invite_link"]
    is_admin: Literal[False]
    team_name: NonEmptyStr = Field(max_length=30, min_length=1)


class RandomParticipantInputData(BaseParticipantData):
    registration_type: Literal["random"]


class ParticipantRequestBody(BaseModel):
    registration_info: Union[AdminParticipantInputData, InviteLinkParticipantInputData, RandomParticipantInputData] = (
        Field(discriminator="registration_type")
    )
