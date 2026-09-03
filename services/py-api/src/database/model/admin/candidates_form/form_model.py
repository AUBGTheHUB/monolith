from dataclasses import dataclass
from typing import Any

from src.database.model.admin.candidates_form.question_model import Question
from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class CandidateForm(BaseDbModel):
    questions: list[Question]

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "questions": self.questions,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "questions": self.questions,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateCandidateFormParams(UpdateParams):
    questions: list[Question] | None = None
