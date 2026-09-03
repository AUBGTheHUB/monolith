from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.candidates_form.question_model import Question
from src.database.repository.admin.candidates_form.questions_repository import QuestionsRepository
from src.exception import QuestionNotFoundError
from src.server.schemas.request_schemas.admin.candidates_form.question_schemas import (
    QuestionPostReqData,
)
from src.service.admin.candidates_form.questions_service import QuestionsService
from tests.unit_tests.conftest import QuestionsRepoMock


@pytest.fixture
def questions_service(questions_repo_mock: QuestionsRepoMock) -> QuestionsService:
    return QuestionsService(
        repo=cast(QuestionsRepository, questions_repo_mock),
    )


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    questions_service: QuestionsService, questions_repo_mock: QuestionsRepoMock, question_mock: Question
) -> None:
    questions = [question_mock]
    questions_repo_mock.fetch_all.return_value = Ok(questions)

    result = await questions_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == questions
    questions_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    questions_service: QuestionsService,
    questions_repo_mock: QuestionsRepoMock,
    question_mock: Question,
) -> None:
    questions_repo_mock.fetch_by_id.return_value = Ok(question_mock)

    result = await questions_service.get(str(question_mock.id))

    assert result.is_ok()
    assert result.unwrap() == question_mock
    questions_repo_mock.fetch_by_id.assert_awaited_once_with(str(question_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    questions_service: QuestionsService, questions_repo_mock: QuestionsRepoMock
) -> None:
    questions_repo_mock.fetch_by_id.return_value = Err(QuestionNotFoundError())

    result = await questions_service.get("missing question")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), QuestionNotFoundError)
    questions_repo_mock.fetch_by_id.assert_awaited_once_with("missing question")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    questions_service: QuestionsService,
    questions_repo_mock: QuestionsRepoMock,
    question_mock: Question,
) -> None:
    req = QuestionPostReqData(
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        options=question_mock.options,
    )

    questions_repo_mock.create.return_value = Ok(question_mock)

    result = await questions_service.create(
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        options=question_mock.options,
    )

    assert result.is_ok()
    questions_repo_mock.create.assert_awaited_once()

    assert questions_repo_mock.create.call_args is not None
    question = questions_repo_mock.create.call_args.args[0]
    assert isinstance(question, Question)
    assert question.prompt == req.prompt
    assert question.question_type == req.question_type
    assert question.answer_type == req.answer_type
    assert question.options == question_mock.options


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    questions_service: QuestionsService, questions_repo_mock: QuestionsRepoMock, question_mock: Question
) -> None:
    updated = Question(
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        options=question_mock.options,
        answer=question_mock.answer,
    )

    questions_repo_mock.update.return_value = Ok(updated)

    result = await questions_service.update(
        question_id=str(question_mock.id),
        prompt=question_mock.prompt,
        question_type=question_mock.question_type,
        answer_type=question_mock.answer_type,
        options=question_mock.options,
        answer=question_mock.answer,
    )

    assert result.is_ok()
    questions_repo_mock.update.assert_awaited_once()

    assert questions_repo_mock.update.call_args is not None
    assert questions_repo_mock.update.call_args.args[0] == question_mock.id

    body = result.ok_value
    assert body.prompt == updated.prompt
    assert body.question_type == updated.question_type
    assert body.answer_type == updated.answer_type
    assert body.options == updated.options


@pytest.mark.asyncio
async def test_delete_calls_repo(
    questions_service: QuestionsService,
    questions_repo_mock: QuestionsRepoMock,
    question_mock: Question,
) -> None:
    questions_repo_mock.delete.return_value = Ok(question_mock)

    result = await questions_service.delete(str(question_mock.id))

    assert result.is_ok()

    questions_repo_mock.delete.assert_awaited_once_with(str(question_mock.id))
