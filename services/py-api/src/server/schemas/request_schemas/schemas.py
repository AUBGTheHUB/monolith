from typing import Optional, Self
from pydantic import EmailStr, BaseModel, model_validator


# https://fastapi.tiangolo.com/tutorial/body/


class ParticipantRequestBody(BaseModel):
    name: str
    email: EmailStr
    team_name: Optional[str] = None
    is_admin: bool

    # https://docs.pydantic.dev/latest/concepts/validators/#before-after-wrap-and-plain-validators
    # https://docs.pydantic.dev/latest/concepts/validators/#model-validators
    @model_validator(mode="after")
    def check_team_name_when_admin_is_true(self) -> Self:
        if self.is_admin and self.team_name is None:
            raise ValueError("Field `team_name` is required when `is_admin=True`")

        return self
