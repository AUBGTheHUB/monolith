from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.candidates_form.form_model import CandidateForm
from src.database.model.admin.candidates_form.question_model import QuestionParams, Question
from src.exception import CandidateFormNotFoundError
from src.server.handlers.admin.candidates_form.forms_handlers import CandidateFormsHandlers
from src.server.schemas.request_schemas.admin.candidates_form.form_schemas import (
    CandidateFormPostReqData,
    CandidateFormPatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.candidates_form.forms_service import CandidateFormsService
from tests.unit_tests.conftest import CandidateFormsServiceMock


@pytest.fixture
def candidate_forms_handlers(candidate_forms_service_mock: CandidateFormsServiceMock) -> CandidateFormsHandlers:
    return CandidateFormsHandlers(cast(CandidateFormsService, candidate_forms_service_mock))


@pytest.mark.asyncio
async def test_create_candidate_form_returns_201(
    candidate_forms_handlers: CandidateFormsHandlers,
    candidate_forms_service_mock: CandidateFormsServiceMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_service_mock.create.return_value = Ok(candidate_form_mock)

    request = CandidateFormPostReqData(
        questions=[
            QuestionParams(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ]
    )
    resp = await candidate_forms_handlers.create_form(request)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    candidate_forms_service_mock.create.assert_awaited_once()

    result = candidate_forms_service_mock.create.call_args
    assert result is not None

    questions = result.kwargs["questions"]
    assert len(questions) == 1
    question = questions[0]

    assert isinstance(question, Question)
    assert question.prompt == "A question"
    assert question.options == []
    assert question.answer == "an answer"
    assert question.question_type == "PR"
    assert question.answer_type == "TEXT"


@pytest.mark.asyncio
async def test_get_all_candidate_forms_returns_200(
    candidate_forms_handlers: CandidateFormsHandlers,
    candidate_forms_service_mock: CandidateFormsServiceMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_service_mock.get_all.return_value = Ok([candidate_form_mock])

    resp = await candidate_forms_handlers.get_all_forms()

    assert resp.status_code == 200
    candidate_forms_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_candidate_form_returns_200(
    candidate_forms_handlers: CandidateFormsHandlers,
    candidate_forms_service_mock: CandidateFormsServiceMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_service_mock.get.return_value = Ok(candidate_form_mock)

    resp = await candidate_forms_handlers.get_form(str(candidate_form_mock.id))

    assert resp.status_code == 200
    candidate_forms_service_mock.get.assert_awaited_once_with(str(candidate_form_mock.id))


@pytest.mark.asyncio
async def test_update_candidate_form_returns_200(
    candidate_forms_handlers: CandidateFormsHandlers,
    candidate_forms_service_mock: CandidateFormsServiceMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_service_mock.update.return_value = Ok(candidate_form_mock)
    request = CandidateFormPatchReqData(
        questions=[
            QuestionParams(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ]
    )

    resp = await candidate_forms_handlers.update_form(str(candidate_form_mock.id), request=request)

    assert resp.status_code == 200
    candidate_forms_service_mock.update.assert_awaited_once_with(
        candidate_form_id=str(candidate_form_mock.id),
        questions=[
            QuestionParams(prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT")
        ],
    )


@pytest.mark.asyncio
async def test_delete_candidate_form_returns_200(
    candidate_forms_handlers: CandidateFormsHandlers,
    candidate_forms_service_mock: CandidateFormsServiceMock,
    candidate_form_mock: CandidateForm,
) -> None:
    candidate_forms_service_mock.delete.return_value = Ok(candidate_form_mock)

    resp = await candidate_forms_handlers.delete_form(str(candidate_form_mock.id))

    assert resp.status_code == 200
    candidate_forms_service_mock.delete.assert_awaited_once_with(str(candidate_form_mock.id))


@pytest.mark.asyncio
async def test_get_candidate_form_returns_404_when_missing(
    candidate_forms_handlers: CandidateFormsHandlers, candidate_forms_service_mock: CandidateFormsServiceMock
) -> None:
    candidate_forms_service_mock.get.return_value = Err(CandidateFormNotFoundError())

    resp = await candidate_forms_handlers.get_form("missing candidate form")

    assert resp.status_code == 404
    candidate_forms_service_mock.get.assert_awaited_once_with("missing candidate form")
