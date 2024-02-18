from typing import Annotated, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, validator

TSHIRT_SIZE = Literal["S", "M", "L", "XL"]

UNIVERSITIES_LIST = Literal[
    "Sofia University",
    "Technical University - Sofia", "American University in Bulgaria", "Plovdiv University", "Other",
]

ALLOWED_AGE = Annotated[int, Field(ge=18, le=99)]

REFERRAL_SOURCES_LIST = Literal[
    "University",
    "Friends", "I was on a previous edition of Hack AUBG",
]

PROGRAMMING_LANGUAGES_LIST = Literal[
    "Frontend Programming", "Backend Programming", "Programming in C#",
    "Programming in Java", "Programming in Python", "Programming in JavaScript", "Other",
]

PROGRAMMING_LEVELS_LIST = Literal[
    "Beginner", "Intermediate",
    "Advanced", "I am not participating as a programmer", "Other",
]


class NewParticipant(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    tshirt_size: TSHIRT_SIZE
    team_name: Optional[str] = None
    is_verified: Optional[bool] = False
    is_admin: Optional[bool] = False
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
    newsletter_consent: bool
    share_info_with_sponsors: bool

    @validator("share_info_with_sponsors")
    def check_if_true(cls, value: bool) -> bool:
        if not value:
            raise ValueError("share_info_with_sponsors shall be true")
        return value


class UpdateParticipant(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    tshirt_size: Optional[TSHIRT_SIZE] = None
    team_name: Optional[str] = None
    is_verified: Optional[bool] = None
    university: Optional[UNIVERSITIES_LIST] = None
    location: Optional[str] = None
    age: Optional[ALLOWED_AGE] = None
    source_of_referral: Optional[REFERRAL_SOURCES_LIST] = None
    programming_language: Optional[PROGRAMMING_LANGUAGES_LIST] = None
    programming_level: Optional[PROGRAMMING_LEVELS_LIST] = None
    has_participated_in_hackaubg: Optional[bool] = None
    has_internship_interest: Optional[bool] = None
    has_participated_in_hackathons: Optional[bool] = None
    has_previous_coding_experience: Optional[bool] = None
    newsletter_consent: Optional[bool] = None
    share_info_with_sponsors: Optional[bool] = True
