from typing import Any, Optional, List, Dict, Literal, cast
from pydantic import BaseModel, HttpUrl, ConfigDict
from src.server.schemas.common.inputs import NonEmptyStr


class BasePatchReqData(BaseModel):
    def model_dump(
        self,
        *,
        mode: str | Any = "python",
        include: Any | None = None,
        exclude: Any | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Any = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            super().model_dump(
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
            ),
        )


class JudgeBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    linkedin_url: Optional[HttpUrl] = None


class JudgePostReqData(JudgeBaseInputData):
    pass


class JudgePatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None


# Sponsors
class SponsorBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    tier: Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]
    logo_url: HttpUrl
    website_url: Optional[HttpUrl] = None


class SponsorPostReqData(SponsorBaseInputData):
    pass


class SponsorPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    tier: Optional[Literal["PLATINUM", "GOLD", "SILVER", "BRONZE", "CUSTOM"]] = None
    logo_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None


# Mentors
class MentorBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    company: NonEmptyStr
    job_title: NonEmptyStr
    avatar_url: HttpUrl
    expertise_areas: List[NonEmptyStr] = []
    linkedin_url: Optional[HttpUrl] = None


class MentorPostReqData(MentorBaseInputData):
    pass


class MentorPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    company: Optional[NonEmptyStr] = None
    job_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    expertise_areas: Optional[List[NonEmptyStr]] = None
    linkedin_url: Optional[HttpUrl] = None


# Hub Members
class HubMemberBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NonEmptyStr
    role_title: NonEmptyStr
    avatar_url: HttpUrl
    social_links: Dict[str, HttpUrl] = {}


class HubMemberPostReqData(HubMemberBaseInputData):
    pass


class HubMemberPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    name: Optional[NonEmptyStr] = None
    role_title: Optional[NonEmptyStr] = None
    avatar_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, HttpUrl]] = None


# Past Events
class PastEventBaseInputData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: NonEmptyStr
    cover_picture: HttpUrl
    tags: List[NonEmptyStr] = []


class PastEventPostReqData(PastEventBaseInputData):
    pass


class PastEventPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    title: Optional[NonEmptyStr] = None
    cover_picture: Optional[HttpUrl] = None
    tags: Optional[List[NonEmptyStr]] = None
