from datetime import datetime
from typing import Tuple, Dict, Any, cast

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err
from bson import ObjectId

from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.mongo.db_manager import PARTICIPANTS_COLLECTION, MongoDatabaseManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.exception import DuplicateEmailError, ParticipantNotFoundError
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> ParticipantsRepository:
    return ParticipantsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock), PARTICIPANTS_COLLECTION)


@pytest.mark.asyncio
async def test_create_participant_success(
    ten_sec_window: Tuple[datetime, datetime],
    mock_random_participant: Participant,
    repo: ParticipantsRepository,
) -> None:

    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(mock_random_participant)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)
    assert result.ok_value.name == mock_random_participant.name
    assert result.ok_value.email == mock_random_participant.email
    assert result.ok_value.is_admin is mock_random_participant.is_admin
    assert result.ok_value.email_verified is mock_random_participant.email_verified
    assert result.ok_value.team_id is mock_random_participant.team_id
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_participant_duplicate_email_error(
    mongo_db_manager_mock: MongoDbManagerMock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:

    # Given
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate email
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate email error")
    )

    # When
    result = await repo.create(mock_random_participant)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    # Check that the error message is the duplicate email as expected
    assert str(result.err_value) == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_create_participant_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:

    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(mock_random_participant)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    mock_obj_id: str,
    mock_admin_participant_dump_no_id: Dict[str, Any],
    repo: ParticipantsRepository,
) -> None:

    # Given
    # Since the id is projected in the actual find_one_and_delete we shall do a deep copy of the mock_admin_participant without the id
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=mock_admin_participant_dump_no_id
    )

    # When
    result = await repo.delete(mock_obj_id)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)

    assert result.ok_value.id == ObjectId(mock_obj_id)
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.email_verified == False


@pytest.mark.asyncio
async def test_delete_participant_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(mock_obj_id)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=Exception())

    # When
    result = await repo.delete(mock_obj_id)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_participant_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    mock_obj_id: str,
    repo: ParticipantsRepository,
    mock_admin_participant_dump_verified: Dict[str, Any],
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=mock_admin_participant_dump_verified
    )

    # When
    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(mock_obj_id)
    assert result.ok_value.email_verified is True
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.is_admin is True
    assert result.ok_value.team_id is not None


@pytest.mark.asyncio
async def test_update_participant_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:

    # Given
    # When a participant with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    mock_db_cursor: MotorDbCursorMock,
    repo: ParticipantsRepository,
    mock_admin_participant: Participant,
) -> None:

    # Given
    # Prepare mock MongoDB documents
    mock_participants_data = [mock_admin_participant.dump_as_mongo_db_document() for _ in range(5)]
    mock_db_cursor.to_list.return_value = mock_participants_data
    # Patch find() to return the mock cursor
    mongo_db_manager_mock.get_collection.return_value.find.return_value = mock_db_cursor

    # When
    # Run the method
    result = await repo.fetch_all()

    # Then
    # Assertions
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, participant in enumerate(result.ok_value):
        assert participant.name == mock_participants_data[i]["name"]
        assert participant.email == mock_participants_data[i]["email"]
        assert participant.is_admin == mock_participants_data[i]["is_admin"]
        assert participant.email_verified == mock_participants_data[i]["email_verified"]
        assert participant.team_id == mock_participants_data[i]["team_id"]
        assert participant.id == str(mock_participants_data[i]["id"])


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: MongoDbManagerMock,
    mock_db_cursor: MotorDbCursorMock,
    repo: ParticipantsRepository,
) -> None:

    # Given
    mock_db_cursor.to_list.return_value = []
    mongo_db_manager_mock.get_collection.return_value.find.return_value = mock_db_cursor

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 0


@pytest.mark.asyncio
async def test_fetch_all_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    mock_db_cursor: MotorDbCursorMock,
    repo: ParticipantsRepository,
) -> None:

    # Given
    mock_db_cursor.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = mock_db_cursor

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
