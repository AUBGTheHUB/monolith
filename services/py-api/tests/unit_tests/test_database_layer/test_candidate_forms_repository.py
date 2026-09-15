from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.candidates_form.form_model import CandidateForm, UpdateCandidateFormParams
from src.database.model.admin.candidates_form.question_model import QuestionParams, Question
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.candidates_form.forms_repository import CandidateFormsRepository
from src.exception import CandidateFormNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MongoDbCursorMock


def _validate_fields(expected: CandidateForm, actual: CandidateForm) -> bool:
    return str(actual.id) == str(expected.id) and actual.questions == expected.questions


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> CandidateFormsRepository:
    return CandidateFormsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_candidate_form_success(
    ten_sec_window: tuple[datetime, datetime],
    candidate_form_mock: CandidateForm,
    repo: CandidateFormsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(candidate_form_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, CandidateForm)
    assert _validate_fields(response.ok_value, candidate_form_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_candidate_form_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, candidate_form_mock: CandidateForm, repo: CandidateFormsRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(candidate_form_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_candidate_form_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    candidate_form_mock_document: dict[str, Any],
    obj_id_mock: str,
    repo: CandidateFormsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=candidate_form_mock_document
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, CandidateForm)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_candidate_form_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: CandidateFormsRepository
) -> None:
    # Given
    # When the candidate_form with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, CandidateFormNotFoundError)


@pytest.mark.asyncio
async def test_delete_candidate_form_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: CandidateFormsRepository
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
async def test_update_candidate_form_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    candidate_form_mock_document: dict[str, Any],
    repo: CandidateFormsRepository,
) -> None:
    # Given
    candidate_form_mock_document["questions"] = [
        {
            "_id": obj_id_mock,
            "prompt": "A question",
            "options": [],
            "answer": "an answer",
            "question_type": "PR",
            "answer_type": "TEXT",
            "created_at": candidate_form_mock_document["created_at"],
            "updated_at": candidate_form_mock_document["updated_at"],
        }
    ]
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=candidate_form_mock_document
    )

    # When
    response = await repo.update(
        obj_id_mock,
        UpdateCandidateFormParams(
            questions=[
                QuestionParams(
                    prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT"
                )
            ]
        ),
    )

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.questions[0].prompt == "A question"
    assert response.ok_value.questions[0].answer == "an answer"


@pytest.mark.asyncio
async def test_update_candidate_form_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: CandidateFormsRepository
) -> None:
    # Given
    # When a candidate_form with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(
        obj_id_mock,
        UpdateCandidateFormParams(
            questions=[
                QuestionParams(
                    prompt="A question", options=[], answer="an answer", question_type="PR", answer_type="TEXT"
                )
            ]
        ),
    )

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, CandidateFormNotFoundError)


@pytest.mark.asyncio
async def test_update_candidate_form_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: CandidateFormsRepository, obj_id_mock: str
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
    candidate_form_mock_document: dict[str, Any],
    candidate_form_mock: CandidateForm,
    repo: CandidateFormsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=candidate_form_mock_document)

    # When
    response = await repo.fetch_by_id(str(candidate_form_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, CandidateForm)
    assert _validate_fields(candidate_form_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_candidate_form_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: CandidateFormsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, CandidateFormNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: CandidateFormsRepository, obj_id_mock: str
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
    repo: CandidateFormsRepository,
    candidate_form_mock: CandidateForm,
) -> None:
    # Given
    mock_candidate_forms_data = [
        {
            "_id": candidate_form_mock.id,
            "questions": [
                {
                    "_id": question.id,
                    "prompt": question.prompt,
                    "options": question.options,
                    "answer": question.answer,
                    "question_type": question.question_type,
                    "answer_type": question.answer_type,
                    "created_at": question.created_at,
                    "updated_at": question.updated_at,
                }
                for question in candidate_form_mock.questions
            ],
            "created_at": candidate_form_mock.created_at,
            "updated_at": candidate_form_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_candidate_forms_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, candidate_form in enumerate(response.ok_value):
        mock_document = mock_candidate_forms_data[i]

        assert candidate_form.id == mock_document["_id"]
        assert candidate_form.created_at == mock_candidate_forms_data[i]["created_at"]
        assert candidate_form.updated_at == mock_candidate_forms_data[i]["updated_at"]

        assert len(candidate_form.questions) == len(mock_document["questions"])

        for question, mock_question in zip(
            candidate_form.questions,
            mock_document["questions"],
        ):
            assert isinstance(question, Question)
            assert question.id == mock_question["_id"]
            assert question.prompt == mock_question["prompt"]
            assert question.options == mock_question["options"]
            assert question.answer == mock_question["answer"]
            assert question.question_type == mock_question["question_type"]
            assert question.answer_type == mock_question["answer_type"]
            assert question.created_at == mock_question["created_at"]
            assert question.updated_at == mock_question["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MongoDbCursorMock,
    repo: CandidateFormsRepository,
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
    repo: CandidateFormsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
