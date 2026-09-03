from dataclasses import dataclass
from typing import Literal, Any

from src.database.model.base_model import BaseDbModel, UpdateParams

ALLOWED_QUESTION_TYPES = Literal["GENERAL", "DEVELOPMENT", "DESIGN", "PR", "MARKETING", "LOGISTICS"]
ALLOWED_ANSWER_TYPES = Literal["TEXT", "SINGLE_CHOICE", "MULTIPLE_CHOICE"]


@dataclass(kw_only=True)
class Question(BaseDbModel):
    prompt: str
    question_type: ALLOWED_QUESTION_TYPES
    answer_type: ALLOWED_ANSWER_TYPES
    options: list[str] | None = None
    answer: str | list[str] | None = None

    def dump_as_mongo_db_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "prompt": self.prompt,
            "options": self.options,
            "answer": self.answer,
            "question_type": self.question_type,
            "answer_type": self.answer_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def dump_as_json(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "prompt": self.prompt,
            "options": self.options,
            "answer": self.answer,
            "question_type": self.question_type,
            "answer_type": self.answer_type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class UpdateQuestionParams(UpdateParams):
    prompt: str | None = None
    options: list[str] | None = None
    answer: str | list[str] | None = None
    question_type: ALLOWED_QUESTION_TYPES | None = None
    answer_type: ALLOWED_ANSWER_TYPES | None = None
