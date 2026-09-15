from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.database.model.admin.candidates_form.question_model import ALLOWED_QUESTION_TYPES, ALLOWED_ANSWER_TYPES
from src.server.schemas.request_schemas.schemas import NonEmptyStr, BasePatchReqData


class QuestionPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: NonEmptyStr
    question_type: ALLOWED_QUESTION_TYPES
    answer_type: ALLOWED_ANSWER_TYPES
    options: Optional[list[str]] = None


class QuestionPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")

    prompt: Optional[NonEmptyStr] = None
    question_type: Optional[ALLOWED_QUESTION_TYPES] = None
    answer_type: Optional[ALLOWED_ANSWER_TYPES] = None
    answer: Optional[str | list[str]] = None
    options: Optional[list[str]] = None
