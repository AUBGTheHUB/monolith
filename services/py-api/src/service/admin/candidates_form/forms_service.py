from result import Result

from src.database.model.admin.candidates_form.question_model import (
    Question,
    UpdateQuestionParams,
    ALLOWED_QUESTION_TYPES,
    ALLOWED_ANSWER_TYPES,
)
from src.database.repository.admin.candidates_form.questions_repository import QuestionsRepository
from src.exception import QuestionNotFoundError


class QuestionsService:
    def __init__(self, repo: QuestionsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Question], Exception]:
        return await self._repo.fetch_all()

    async def get(self, question_id: str) -> Result[Question, QuestionNotFoundError | Exception]:
        return await self._repo.fetch_by_id(question_id)

    async def create(
        self,
        prompt: str,
        question_type: ALLOWED_QUESTION_TYPES,
        answer_type: ALLOWED_ANSWER_TYPES,
        options: list[str] | None = None,
    ) -> Result[Question, QuestionNotFoundError | Exception]:
        question = Question(prompt=prompt, question_type=question_type, answer_type=answer_type, options=options)

        return await self._repo.create(question)

    async def update(
        self,
        question_id: str,
        prompt: str | None = None,
        question_type: ALLOWED_QUESTION_TYPES | None = None,
        answer_type: ALLOWED_ANSWER_TYPES | None = None,
        answer: str | list[str] | None = None,
        options: list[str] | None = None,
    ) -> Result[Question, QuestionNotFoundError | Exception]:

        params = UpdateQuestionParams(
            prompt=prompt, question_type=question_type, answer_type=answer_type, options=options, answer=answer
        )
        return await self._repo.update(question_id, params)

    async def delete(self, question_id: str) -> Result[Question, QuestionNotFoundError | Exception]:
        return await self._repo.delete(question_id)
