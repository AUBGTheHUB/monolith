from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated, Literal, Dict, Any, Optional, Union
from pydantic import Field, EmailStr, ConfigDict
from bson import ObjectId

from src.database.model.base_model import BaseDbModel, SerializableObjectId, UpdateParams

TSHIRT_SIZE = Literal[
    "Small (S)",
    "Medium (M)",
    "Large (L)",
    "Extra Large (XL)",
]

UNIVERSITIES_LIST = Literal[
    "Sofia University",
    "Technical University - Sofia",
    "American University in Bulgaria",
    "Plovdiv University",
    "Other",
]

ALLOWED_AGE = Annotated[int, Field(ge=16, le=69)]

REFERRAL_SOURCES_LIST = Literal[
    "University",
    "Friends",
    "Social media",
    "I was on a previous edition of Hack AUBG",
    "Other",
]

PROGRAMMING_LANGUAGES_LIST = Literal[
    "Programming in JavaScript",
    "Programming in C#",
    "Programming in C++",
    "Programming in Java",
    "Programming in Python",
    "I don't have experience with any languages",
    "Other",
]

PROGRAMMING_LEVELS_LIST = Literal[
    "Beginner",
    "Intermediate",
    "Advanced",
    "I am not participating as a programmer",
    "Other",
]


@dataclass(kw_only=True)
class Participant(BaseDbModel):
    """A representation of the Participant entity in Mongo. It is also the schema of how the entity should look
    like in Mongo before it is inserted"""

    name: str
    email: str
    is_admin: bool
    email_verified: bool = field(default=False)
    team_id: Optional[SerializableObjectId]
    last_sent_verification_email: Optional[datetime] = field(default=None)
    """The last time a verification email was sent. Used for rate-limiting purposed when the participant clicks
    resend email."""
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

    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        return {
            "_id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "email_verified": self.email_verified,
            "team_id": self.team_id,
            "tshirt_size": self.tshirt_size,
            "university": self.university,
            "location": self.location,
            "age": self.age,
            "source_of_referral": self.source_of_referral,
            "programming_language": self.programming_language,
            "programming_level": self.programming_level,
            "has_participated_in_hackaubg": self.has_participated_in_hackaubg,
            "has_internship_interest": self.has_internship_interest,
            "has_participated_in_hackathons": self.has_participated_in_hackathons,
            "has_previous_coding_experience": self.has_previous_coding_experience,
            "share_info_with_sponsors": self.share_info_with_sponsors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_sent_verification_email": self.last_sent_verification_email,
        }

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "email_verified": self.email_verified,
            "team_id": str(self.team_id) if self.team_id else None,
            "tshirt_size": self.tshirt_size,
            "university": self.university,
            "location": self.location,
            "age": self.age,
            "source_of_referral": self.source_of_referral,
            "programming_language": self.programming_language,
            "programming_level": self.programming_level,
            "has_participated_in_hackaubg": self.has_participated_in_hackaubg,
            "has_internship_interest": self.has_internship_interest,
            "has_participated_in_hackathons": self.has_participated_in_hackathons,
            "has_previous_coding_experience": self.has_previous_coding_experience,
            "share_info_with_sponsors": self.share_info_with_sponsors,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_sent_verification_email": (
                self.last_sent_verification_email.strftime("%Y-%m-%d %H:%M:%S")
                if self.last_sent_verification_email
                else None
            ),
        }


class UpdateParticipantParams(UpdateParams):
    """This model makes each field of the Participant optional, so that you can
    only set values to the fields that you want to modify and pass to the
    MongoDB find_one_and_update() method.
    Build to be used for updating the Participant document in the database.

    The ``updated_at`` filed us set for you, so you should not set it explicitly
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    email_verified: Union[bool, None] = None
    is_admin: Union[bool, None] = None
    team_id: Union[ObjectId, None] = None
    tshirt_size: Union[TSHIRT_SIZE, None] = None
    university: Union[UNIVERSITIES_LIST, None] = None
    location: Union[str, None] = None
    age: Union[ALLOWED_AGE, None] = None
    source_of_referral: Union[REFERRAL_SOURCES_LIST, None] = None
    programming_language: Union[PROGRAMMING_LANGUAGES_LIST, None] = None
    programming_level: Union[PROGRAMMING_LEVELS_LIST, None] = None
    has_participated_in_hackaubg: Union[bool, None] = None
    has_internship_interest: Union[bool, None] = None
    has_participated_in_hackathons: Union[bool, None] = None
    has_previous_coding_experience: Union[bool, None] = None
    share_info_with_sponsors: Union[bool, None] = None
    last_sent_verification_email: Union[datetime, None] = None

    def model_dump(
        self,
        *,
        mode: str | Any = "python",
        include: Any | None = None,
        exclude: Any | None = ("team_id",),
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Any = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        dump = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        # As team_id is ObjectID, which is not serializable by default, we casually exclude it and add it back to the
        # dump, to avoid Pydantic throwing errors. As model_dump is used primarily in Mongo database operations, it's
        # ok to have the team_id as an ObjectID, because the Motor library expects it like that.
        if self.team_id is not None:
            dump["team_id"] = self.team_id
        return dump
