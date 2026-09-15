from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.candidates_form.question_model import Question
from src.exception import QuestionNotFoundError
from src.server.handlers.admin.candidates_form.questions_handlers import QuestionsHandlers
from src.server.schemas.request_schemas.admin.candidates_form.question_schemas import (
    QuestionPostReqData,
    QuestionPatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.candidates_form.questions_service import QuestionsService
from tests.unit_tests.conftest import QuestionsServiceMock


@pytest.fixture
def questions_handlers(questions_service_mock: QuestionsServiceMock) -> QuestionsHandlers:
    return QuestionsHandlers(cast(QuestionsService, questions_service_mock))


@pytest.mark.asyncio
async def test_create_question_returns_201(
    questions_handlers: QuestionsHandlers, questions_service_mock: QuestionsServiceMock, question_mock: Question
) -> None:
    questions_service_mock.create.return_value = Ok(question_mock)

    request = QuestionPostReqData(
        prompt=question_mock.prompt,
        options=question_mock.options,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
    )
    resp = await questions_handlers.create_question(request)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    questions_service_mock.create.assert_awaited_once_with(
        prompt=question_mock.prompt,
        options=question_mock.options,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
    )


@pytest.mark.asyncio
async def test_get_all_questions_returns_200(
    questions_handlers: QuestionsHandlers,
    questions_service_mock: QuestionsServiceMock,
    question_mock: Question,
) -> None:
    questions_service_mock.get_all.return_value = Ok([question_mock])

    resp = await questions_handlers.get_all_questions()

    assert resp.status_code == 200
    questions_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_question_returns_200(
    questions_handlers: QuestionsHandlers,
    questions_service_mock: QuestionsServiceMock,
    question_mock: Question,
) -> None:
    questions_service_mock.get.return_value = Ok(question_mock)

    resp = await questions_handlers.get_question(str(question_mock.id))

    assert resp.status_code == 200
    questions_service_mock.get.assert_awaited_once_with(str(question_mock.id))


@pytest.mark.asyncio
async def test_update_question_returns_200(
    questions_handlers: QuestionsHandlers, questions_service_mock: QuestionsServiceMock, question_mock: Question
) -> None:
    questions_service_mock.update.return_value = Ok(question_mock)
    request = QuestionPatchReqData(
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        answer=question_mock.answer,
        options=question_mock.options,
    )

    resp = await questions_handlers.update_question(str(question_mock.id), request=request)

    assert resp.status_code == 200
    questions_service_mock.update.assert_awaited_once_with(
        question_id=str(question_mock.id),
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        answer=question_mock.answer,
        options=question_mock.options,
    )


@pytest.mark.asyncio
async def test_delete_question_returns_200(
    questions_handlers: QuestionsHandlers,
    questions_service_mock: QuestionsServiceMock,
    question_mock: Question,
) -> None:
    questions_service_mock.delete.return_value = Ok(question_mock)

    resp = await questions_handlers.delete_question(str(question_mock.id))

    assert resp.status_code == 200
    questions_service_mock.delete.assert_awaited_once_with(str(question_mock.id))


@pytest.mark.asyncio
async def test_get_question_returns_404_when_missing(
    questions_handlers: QuestionsHandlers, questions_service_mock: QuestionsServiceMock
) -> None:
    questions_service_mock.get.return_value = Err(QuestionNotFoundError())

    resp = await questions_handlers.get_question("missing question")

    assert resp.status_code == 404
    questions_service_mock.get.assert_awaited_once_with("missing question")
