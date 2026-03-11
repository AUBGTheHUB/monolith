from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err

from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.judges_repository import JudgesRepository
from src.exception import JudgeNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


def _validate_fields(expected: Judge, actual: Judge) -> bool:
    return (
        str(actual.id) == str(expected.id)
        and actual.name == expected.name
        and actual.company == expected.company
        and actual.linkedin_url == expected.linkedin_url
        and actual.avatar_url == expected.avatar_url
        and actual.job_title == expected.job_title
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> JudgesRepository:
    return JudgesRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_judge_success(
    ten_sec_window: tuple[datetime, datetime],
    judge_mock: Judge,
    repo: JudgesRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(judge_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Judge)
    assert _validate_fields(response.ok_value, judge_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_judge_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, judge_mock: Judge, repo: JudgesRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(judge_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_judge_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    judge_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: JudgesRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=judge_no_id_mock)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Judge)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_judge_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: JudgesRepository
) -> None:
    # Given
    # When the past event with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, JudgeNotFoundError)


@pytest.mark.asyncio
async def test_delete_judge_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: JudgesRepository
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
async def test_update_judge_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    judge_no_id_mock: dict[str, Any],
    repo: JudgesRepository,
) -> None:
    # Given
    judge_no_id_mock["name"] = "Ivan"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=judge_no_id_mock)

    # When
    response = await repo.update(obj_id_mock, UpdateJudgeParams(name="Ivan"))

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.name == "Ivan"


@pytest.mark.asyncio
async def test_update_judge_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: JudgesRepository
) -> None:
    # Given
    # When a sponsor with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(obj_id_mock, UpdateJudgeParams(name="Ivan"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, JudgeNotFoundError)


@pytest.mark.asyncio
async def test_update_judge_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: JudgesRepository, obj_id_mock: str
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
    judge_no_id_mock: dict[str, Any],
    judge_mock: Judge,
    repo: JudgesRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=judge_no_id_mock)

    # When
    response = await repo.fetch_by_id(str(judge_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Judge)
    assert _validate_fields(judge_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_judge_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: JudgesRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, JudgeNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: JudgesRepository, obj_id_mock: str
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
    db_cursor_mock: MotorDbCursorMock,
    repo: JudgesRepository,
    judge_mock: Judge,
) -> None:
    # Given
    mock_judges_data = [
        {
            "_id": judge_mock.id,
            "name": judge_mock.name,
            "company": judge_mock.company,
            "avatar_url": judge_mock.avatar_url,
            "job_title": judge_mock.job_title,
            "linkedin_url": judge_mock.linkedin_url,
            "created_at": judge_mock.created_at,
            "updated_at": judge_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_judges_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, judge in enumerate(response.ok_value):
        assert judge.name == mock_judges_data[i]["name"]
        assert judge.job_title == mock_judges_data[i]["job_title"]
        assert judge.company == mock_judges_data[i]["company"]
        assert judge.avatar_url == mock_judges_data[i]["avatar_url"]
        assert judge.linkedin_url == mock_judges_data[i]["linkedin_url"]
        assert judge.created_at == mock_judges_data[i]["created_at"]
        assert judge.updated_at == mock_judges_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: JudgesRepository,
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
    db_cursor_mock: MotorDbCursorMock,
    repo: JudgesRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
