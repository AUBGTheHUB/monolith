from __future__ import annotations

from typing import cast

import pytest
from bson import ObjectId
from result import Err, Ok

from src.database.model.admin.candidates_form.form_model import CandidateForm
from src.database.model.admin.candidates_form.question_model import QuestionParams, Question
from src.database.repository.admin.candidates_form.forms_repository import CandidateFormsRepository
from src.exception import CandidateFormNotFoundError
from src.service.admin.candidates_form.forms_service import CandidateFormsService
from tests.unit_tests.conftest import CandidateFormsRepoMock


@pytest.fixture
def candidate_forms_service(candidate_forms_repo_mock: CandidateFormsRepoMock) -> CandidateFormsService:
    return CandidateFormsService(
        repo=cast(CandidateFormsRepository, candidate_forms_repo_mock),
    )


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    candidate_forms_service: CandidateFormsService,
    candidate_forms_repo_mock: CandidateFormsRepoMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms = [candidate_form_mock]
    candidate_forms_repo_mock.fetch_all.return_value = Ok(candidate_forms)

    result = await candidate_forms_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == candidate_forms
    candidate_forms_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    candidate_forms_service: CandidateFormsService,
    candidate_forms_repo_mock: CandidateFormsRepoMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_repo_mock.fetch_by_id.return_value = Ok(candidate_form_mock)

    result = await candidate_forms_service.get(str(candidate_form_mock.id))

    assert result.is_ok()
    assert result.unwrap() == candidate_form_mock
    candidate_forms_repo_mock.fetch_by_id.assert_awaited_once_with(str(candidate_form_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    candidate_forms_service: CandidateFormsService, candidate_forms_repo_mock: CandidateFormsRepoMock
) -> None:
    candidate_forms_repo_mock.fetch_by_id.return_value = Err(CandidateFormNotFoundError())

    result = await candidate_forms_service.get("missing candidate form")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), CandidateFormNotFoundError)
    candidate_forms_repo_mock.fetch_by_id.assert_awaited_once_with("missing candidate form")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    candidate_forms_service: CandidateFormsService,
    candidate_forms_repo_mock: CandidateFormsRepoMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_repo_mock.create.return_value = Ok(candidate_form_mock)

    result = await candidate_forms_service.create(
        questions=[
            Question(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ]
    )

    assert result.is_ok()
    candidate_forms_repo_mock.create.assert_awaited_once()

    assert candidate_forms_repo_mock.create.call_args is not None
    candidate_form = candidate_forms_repo_mock.create.call_args.args[0]
    assert isinstance(candidate_form, CandidateForm)
    assert len(candidate_form.questions) == 1

    question = candidate_form.questions[0]

    assert question.prompt == "A question"
    assert question.options == []
    assert question.answer == "an answer"
    assert question.question_type == "PR"
    assert question.answer_type == "TEXT"

    assert isinstance(question.id, ObjectId)
    assert question.created_at is not None
    assert question.updated_at is not None


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    candidate_forms_service: CandidateFormsService,
    candidate_forms_repo_mock: CandidateFormsRepoMock,
    candidate_form_mock: CandidateForm,
) -> None:
    updated = CandidateForm(
        questions=[
            Question(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ]
    )

    candidate_forms_repo_mock.update.return_value = Ok(updated)

    result = await candidate_forms_service.update(
        candidate_form_id=str(candidate_form_mock.id),
        questions=[
            QuestionParams(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ],
    )

    assert result.is_ok()
    candidate_forms_repo_mock.update.assert_awaited_once()

    assert candidate_forms_repo_mock.update.call_args is not None
    assert candidate_forms_repo_mock.update.call_args.args[0] == str(candidate_form_mock.id)

    body = result.ok_value
    assert len(body.questions) == 1

    question = body.questions[0]

    assert question.prompt == "A question"
    assert question.options == []
    assert question.answer == "an answer"
    assert question.question_type == "PR"
    assert question.answer_type == "TEXT"

    assert isinstance(question.id, ObjectId)
    assert question.created_at is not None
    assert question.updated_at is not None


@pytest.mark.asyncio
async def test_delete_calls_repo(
    candidate_forms_service: CandidateFormsService,
    candidate_forms_repo_mock: CandidateFormsRepoMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_repo_mock.delete.return_value = Ok(candidate_form_mock)

    result = await candidate_forms_service.delete(str(candidate_form_mock.id))

    assert result.is_ok()

    candidate_forms_repo_mock.delete.assert_awaited_once_with(str(candidate_form_mock.id))
