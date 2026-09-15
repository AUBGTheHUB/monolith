from result import Result

from src.database.model.admin.candidates_form.form_model import (
    CandidateForm,
    UpdateCandidateFormParams,
)
from src.database.model.admin.candidates_form.question_model import Question, QuestionParams
from src.database.repository.admin.candidates_form.forms_repository import CandidateFormsRepository
from src.exception import CandidateFormNotFoundError


class CandidateFormsService:
    def __init__(self, repo: CandidateFormsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[CandidateForm], Exception]:
        return await self._repo.fetch_all()

    async def get(self, candidate_form_id: str) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        return await self._repo.fetch_by_id(candidate_form_id)

    async def create(
        self,
        questions: list[Question],
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        candidate_form = CandidateForm(questions=questions)

        return await self._repo.create(candidate_form)

    async def update(
        self,
        candidate_form_id: str,
        questions: list[QuestionParams],
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:

        params = UpdateCandidateFormParams(questions=questions)
        return await self._repo.update(candidate_form_id, params)

    async def delete(self, candidate_form_id: str) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        return await self._repo.delete(candidate_form_id)
