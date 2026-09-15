from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.candidates_form.question_model import Question, UpdateQuestionParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.candidates_form.questions_repository import QuestionsRepository
from src.exception import QuestionNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MongoDbCursorMock


def _validate_fields(expected: Question, actual: Question) -> bool:
    return (
        str(actual.id) == str(expected.id)
        and actual.prompt == expected.prompt
        and actual.options == expected.options
        and actual.answer == expected.answer
        and actual.question_type == expected.question_type
        and actual.answer_type == expected.answer_type
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> QuestionsRepository:
    return QuestionsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_question_success(
    ten_sec_window: tuple[datetime, datetime],
    question_mock: Question,
    repo: QuestionsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(question_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Question)
    assert _validate_fields(response.ok_value, question_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_question_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, question_mock: Question, repo: QuestionsRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(question_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_question_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    question_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: QuestionsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=question_no_id_mock)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Question)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_question_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: QuestionsRepository
) -> None:
    # Given
    # When the question with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, QuestionNotFoundError)


@pytest.mark.asyncio
async def test_delete_question_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: QuestionsRepository
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_update_question_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    question_no_id_mock: dict[str, Any],
    repo: QuestionsRepository,
) -> None:
    # Given
    question_no_id_mock["prompt"] = "New Question"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=question_no_id_mock)

    # When
    response = await repo.update(obj_id_mock, UpdateQuestionParams(prompt="New Question"))

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.prompt == "New Question"


@pytest.mark.asyncio
async def test_update_question_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: QuestionsRepository
) -> None:
    # Given
    # When a question with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(obj_id_mock, UpdateQuestionParams(prompt="New Question"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, QuestionNotFoundError)


@pytest.mark.asyncio
async def test_update_question_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: QuestionsRepository, obj_id_mock: str
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    question_no_id_mock: dict[str, Any],
    question_mock: Question,
    repo: QuestionsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=question_no_id_mock)

    # When
    response = await repo.fetch_by_id(str(question_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Question)
    assert _validate_fields(question_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_question_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: QuestionsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, QuestionNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: QuestionsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: QuestionsRepository,
    question_mock: Question,
) -> None:
    # Given
    mock_questions_data = [
        {
            "_id": question_mock.id,
            "prompt": question_mock.prompt,
            "options": question_mock.options,
            "answer": question_mock.answer,
            "question_type": question_mock.question_type,
            "answer_type": question_mock.answer_type,
            "created_at": question_mock.created_at,
            "updated_at": question_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_questions_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, question in enumerate(response.ok_value):
        assert question.prompt == mock_questions_data[i]["prompt"]
        assert question.options == mock_questions_data[i]["options"]
        assert question.answer == mock_questions_data[i]["answer"]
        assert question.question_type == mock_questions_data[i]["question_type"]
        assert question.answer_type == mock_questions_data[i]["answer_type"]
        assert question.created_at == mock_questions_data[i]["created_at"]
        assert question.updated_at == mock_questions_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MongoDbCursorMock,
    repo: QuestionsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = []
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 0


@pytest.mark.asyncio
async def test_fetch_all_error(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MongoDbCursorMock,
    repo: QuestionsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
