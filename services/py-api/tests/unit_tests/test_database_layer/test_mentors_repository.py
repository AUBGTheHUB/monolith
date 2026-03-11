from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.exception import MentorNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


def _validate_fields(expected: Mentor, actual: Mentor) -> bool:
    return (
        str(actual.id) == str(expected.id)
        and actual.name == expected.name
        and actual.company == expected.company
        and actual.job_title == expected.job_title
        and actual.avatar_url == expected.avatar_url
        and actual.linkedin_url == expected.linkedin_url
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> MentorsRepository:
    return MentorsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_mentor_success(
    ten_sec_window: tuple[datetime, datetime],
    mentor_mock: Mentor,
    repo: MentorsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(mentor_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Mentor)
    assert _validate_fields(response.ok_value, mentor_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_mentor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, mentor_mock: Mentor, repo: MentorsRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(mentor_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_mentor_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    mentor_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: MentorsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=mentor_no_id_mock)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Mentor)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_mentor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: MentorsRepository
) -> None:
    # Given
    # When the mentor with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, MentorNotFoundError)


@pytest.mark.asyncio
async def test_delete_mentor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: MentorsRepository
) -> None:
    # Given
    # Simulate a general exception raised by find_one_and_delete
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
async def test_update_mentor_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    mentor_no_id_mock: dict[str, Any],
    repo: MentorsRepository,
) -> None:
    # Given
    mentor_no_id_mock["name"] = "Jane A. Doe"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=mentor_no_id_mock)

    # When
    response = await repo.update(obj_id_mock, UpdateMentorParams(name="Jane A. Doe"))

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.name == "Jane A. Doe"


@pytest.mark.asyncio
async def test_update_mentor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: MentorsRepository
) -> None:
    # Given
    # When a mentor with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(obj_id_mock, UpdateMentorParams(name="Jane A. Doe"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, MentorNotFoundError)


@pytest.mark.asyncio
async def test_update_mentor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: MentorsRepository, obj_id_mock: str
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    response = await repo.update(obj_id_mock, UpdateMentorParams(name="Jane A. Doe"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    mentor_no_id_mock: dict[str, Any],
    mentor_mock: Mentor,
    repo: MentorsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=mentor_no_id_mock)

    # When
    response = await repo.fetch_by_id(str(mentor_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Mentor)
    assert _validate_fields(mentor_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_mentor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: MentorsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, MentorNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: MentorsRepository, obj_id_mock: str
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
    repo: MentorsRepository,
    mentor_mock: Mentor,
) -> None:
    # Given
    mock_mentors_data = [
        {
            "_id": mentor_mock.id,
            "name": mentor_mock.name,
            "company": mentor_mock.company,
            "job_title": mentor_mock.job_title,
            "avatar_url": mentor_mock.avatar_url,
            "linkedin_url": mentor_mock.linkedin_url,
            "created_at": mentor_mock.created_at,
            "updated_at": mentor_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_mentors_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, mentor in enumerate(response.ok_value):
        assert mentor.name == mock_mentors_data[i]["name"]
        assert mentor.company == mock_mentors_data[i]["company"]
        assert mentor.job_title == mock_mentors_data[i]["job_title"]
        assert mentor.avatar_url == mock_mentors_data[i]["avatar_url"]
        assert mentor.linkedin_url == mock_mentors_data[i]["linkedin_url"]
        assert mentor.created_at == mock_mentors_data[i]["created_at"]
        assert mentor.updated_at == mock_mentors_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: MentorsRepository,
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
    repo: MentorsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list = AsyncMock(side_effect=Exception("Test error"))
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    assert str(response.err_value) == "Test error"
