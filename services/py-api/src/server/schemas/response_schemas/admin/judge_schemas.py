from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.judge_model import Judge


class JudgeResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    judge: Judge

    @field_serializer("judge")
    def serialize_judge(self, judge: Judge) -> dict[str, Any]:
        return judge.dump_as_json()
