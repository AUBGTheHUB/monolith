from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.event.attendee_model import Attendee, UpdateAttendeeParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.event.attendees_repository import AttendeesRepository
from src.exception import AttendeeNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MongoDbCursorMock


def _validate_fields(expected: Attendee, actual: Attendee) -> bool:
    return (
        str(actual.id) == str(expected.id)
        and actual.name == expected.name
        and actual.email == expected.email
        and actual.has_paid == expected.has_paid
        and actual.ticket_type == expected.ticket_type
        and actual.ticket_serial_number == actual.ticket_serial_number
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> AttendeesRepository:
    return AttendeesRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_attendee_success(
    ten_sec_window: tuple[datetime, datetime],
    attendee_mock: Attendee,
    repo: AttendeesRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(attendee_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Attendee)
    assert _validate_fields(response.ok_value, attendee_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_attendee_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, attendee_mock: Attendee, repo: AttendeesRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(attendee_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_attendee_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    attendee_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: AttendeesRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=attendee_no_id_mock)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Attendee)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_attendee_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: AttendeesRepository
) -> None:
    # Given
    # When the past event with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, AttendeeNotFoundError)


@pytest.mark.asyncio
async def test_delete_attendee_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: AttendeesRepository
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
async def test_update_attendee_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    attendee_no_id_mock: dict[str, Any],
    repo: AttendeesRepository,
) -> None:
    # Given
    attendee_no_id_mock["name"] = "Gosho"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=attendee_no_id_mock)

    # When
    response = await repo.update(obj_id_mock, UpdateAttendeeParams(name="Gosho"))

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.name == "Gosho"


@pytest.mark.asyncio
async def test_update_attendee_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: AttendeesRepository
) -> None:
    # Given
    # When a attendee with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(obj_id_mock, UpdateAttendeeParams(name="Gosho"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, AttendeeNotFoundError)


@pytest.mark.asyncio
async def test_update_attendee_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: AttendeesRepository, obj_id_mock: str
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
    attendee_no_id_mock: dict[str, Any],
    attendee_mock: Attendee,
    repo: AttendeesRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=attendee_no_id_mock)

    # When
    response = await repo.fetch_by_id(str(attendee_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Attendee)
    assert _validate_fields(attendee_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_attendee_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: AttendeesRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, AttendeeNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: AttendeesRepository, obj_id_mock: str
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
    repo: AttendeesRepository,
    attendee_mock: Attendee,
) -> None:
    # Given
    mock_attendees_data = [
        {
            "_id": attendee_mock.id,
            "name": attendee_mock.name,
            "email": attendee_mock.email,
            "has_paid": attendee_mock.has_paid,
            "ticket_type": attendee_mock.ticket_type,
            "ticket_serial_number": attendee_mock.ticket_serial_number,
            "created_at": attendee_mock.created_at,
            "updated_at": attendee_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_attendees_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, attendee in enumerate(response.ok_value):
        assert attendee.name == mock_attendees_data[i]["name"]
        assert attendee.email == mock_attendees_data[i]["email"]
        assert attendee.has_paid == mock_attendees_data[i]["has_paid"]
        assert attendee.ticket_type == mock_attendees_data[i]["ticket_type"]
        assert attendee.ticket_serial_number == mock_attendees_data[i]["ticket_serial_number"]
        assert attendee.created_at == mock_attendees_data[i]["created_at"]
        assert attendee.updated_at == mock_attendees_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MongoDbCursorMock,
    repo: AttendeesRepository,
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
    repo: AttendeesRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
