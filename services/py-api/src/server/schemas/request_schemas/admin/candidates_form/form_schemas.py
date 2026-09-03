from pydantic import BaseModel, ConfigDict

from src.database.model.admin.candidates_form.question_model import QuestionParams
from src.server.schemas.request_schemas.schemas import BasePatchReqData


class CandidateFormPostReqData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    questions: list[QuestionParams]


class CandidatesFormPatchReqData(BasePatchReqData):
    model_config = ConfigDict(extra="forbid")
    questions: list[QuestionParams]
