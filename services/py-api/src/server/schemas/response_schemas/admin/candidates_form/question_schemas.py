from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.candidates_form.question_model import Question


class QuestionResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    question: Question

    @field_serializer("question")
    def serialize_question(self, question: Question) -> dict[str, Any]:
        return question.dump_as_json()


class QuestionsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    questions: list[Question]

    @field_serializer("questions")
    def serialize_question(self, questions: list[Question]) -> list[dict[str, Any]]:
        return [question.dump_as_json() for question in questions]
