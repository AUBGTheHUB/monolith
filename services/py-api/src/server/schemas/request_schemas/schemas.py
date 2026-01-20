from typing import Literal, Any, Annotated, cast

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator
from pydantic.main import IncEx

type NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
"""A Type representing and input of a non-empty string trimmed of whitespace"""


class BasePatchReqData(BaseModel):
    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
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


class FeatureSwitchUpdateBody(BasePatchReqData):
    name: NonEmptyStr
    state: bool


class AdminTeamMemberIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(max_length=100, min_length=1)
    photo_url: str = Field(max_length=500)
    linkedin_url: str = Field(max_length=500)

    @field_validator("linkedin_url")
    @classmethod
    def _check_linkedin_format(cls, v: str) -> str:
        if not v.startswith("https://www.linkedin.com/"):
            raise ValueError("Invalid LinkedIn URL")
        return v


