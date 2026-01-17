from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.exception import PastEventNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> PastEventsRepository:
    return PastEventsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_past_event_success(
    ten_sec_window: tuple[datetime, datetime],
    past_event_mock: PastEvent,
    repo: PastEventsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(past_event_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, PastEvent)
    assert result.ok_value.id == past_event_mock.id
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_past_event_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, past_event_mock: PastEvent, repo: PastEventsRepository
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(past_event_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_past_event_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    past_event_dump_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: PastEventsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=past_event_dump_no_id_mock
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, PastEvent)
    assert result.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: PastEventsRepository
) -> None:
    # Given
    # When the past event with the sepcified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, PastEventNotFoundError)


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: PastEventsRepository
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_update_past_event_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    past_event_dump_no_id_mock: dict[str, Any],
    repo: PastEventsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=past_event_dump_no_id_mock
    )
    past_event_dump_no_id_mock["title"] = "mii"
    # When
    result = await repo.update(obj_id_mock, UpdatePastEventParams(title="mii"))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.title == "mii"


@pytest.mark.asyncio
async def test_update_past_event_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: PastEventsRepository
) -> None:
    # Given
    # When a team with the specified id is not found find_one_and_update returns none
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdatePastEventParams(title="mii"))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, PastEventNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    past_event_dump_no_id_mock: dict[str, Any],
    past_event_mock: PastEvent,
    repo: PastEventsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=past_event_dump_no_id_mock)

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, PastEvent)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.title == past_event_mock.title
    assert result.ok_value.cover_picture == past_event_mock.cover_picture


@pytest.mark.asyncio
async def test_fetch_by_id_past_event_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: PastEventsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, PastEventNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: PastEventsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: PastEventsRepository,
    past_event_mock: PastEvent,
) -> None:
    # Given
    mock_past_events_data = [
        {
            "_id": past_event_mock.id,
            "title": past_event_mock.title,
            "cover_picture": past_event_mock.cover_picture,
            "created_at": past_event_mock.created_at,
            "updated_at": past_event_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_past_events_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, past_event in enumerate(result.ok_value):
        assert past_event.title == mock_past_events_data[i]["title"]
        assert past_event.cover_picture == mock_past_events_data[i]["cover_picture"]
        assert past_event.created_at == mock_past_events_data[i]["created_at"]
        assert past_event.updated_at == mock_past_events_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: PastEventsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = []
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 0


@pytest.mark.asyncio
async def test_fetch_all_error(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: PastEventsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
