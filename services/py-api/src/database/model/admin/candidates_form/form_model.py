from dataclasses import dataclass
from typing import Any, Mapping

from src.database.model.admin.candidates_form.question_model import Question, QuestionParams
from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class CandidateForm(BaseDbModel):
    questions: list[Question]

    @classmethod
    def from_mongo_db_document(
        cls,
        document: Mapping[str, Any],
    ) -> "CandidateForm":
        return cls(
            questions=[
                Question(
                    id=question["_id"],
                    prompt=question["prompt"],
                    options=question.get("options"),
                    answer=question.get("answer"),
                    question_type=question["question_type"],
                    answer_type=question["answer_type"],
                    created_at=question["created_at"],
                    updated_at=question["updated_at"],
                )
                for question in document["questions"]
            ],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "questions": [question.dump_as_mongo_db_document() for question in self.questions],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "questions": [question.dump_as_json() for question in self.questions],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateCandidateFormParams(UpdateParams):
    questions: list[QuestionParams] | None = None
