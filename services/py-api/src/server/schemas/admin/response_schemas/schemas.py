from pydantic import BaseModel, ConfigDict, field_serializer
from src.database.model.admin.judge_model import Judge
from typing import Any


class JudgeResponse(BaseModel):
    """
    Response wrapper for a single Judge document.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    judge: Judge  # DB model instance

    @field_serializer("judge")
    def serialize_judge(self, judge: Judge) -> dict[str, Any]:
        return judge.dump_as_json()
