from datetime import datetime
from typing import Tuple
from unittest.mock import Mock, AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_manager import PARTICIPANTS_COLLECTION
from src.database.model.participant_model import Participant, UpdateParticipantParams
from src.database.repository.participants_repository import ParticipantsRepository
from src.server.exception import DuplicateEmailError, ParticipantNotFoundError
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME


@pytest.fixture
def repo(db_manager_mock: Mock) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager_mock, PARTICIPANTS_COLLECTION)


@pytest.mark.asyncio
async def test_create_participant_success(
    ten_sec_window: Tuple[datetime, datetime],
    mock_random_participant: Participant,
    repo: ParticipantsRepository,
) -> None:
    start_time, end_time = ten_sec_window

    result = await repo.create(mock_random_participant)

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
    db_manager_mock: Mock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate email
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate email error")
    )

    result = await repo.create(mock_random_participant)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    # Check that the error message is the duplicate email as expected
    assert str(result.err_value) == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_create_participant_general_exception(
    db_manager_mock: Mock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:
    # Simulate a general exception raised by insert_one
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.create(mock_random_participant)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_successful(db_manager_mock: Mock, mock_obj_id: str, repo: ParticipantsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value={
            "name": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "is_admin": False,
            "email_verified": False,
            "team_id": mock_obj_id,
        }
    )

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.email_verified == False


@pytest.mark.asyncio
async def test_delete_participant_not_found(
    db_manager_mock: Mock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:

    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(db_manager_mock: Mock, repo: ParticipantsRepository, mock_obj_id: str) -> None:
    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=Exception())

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_participant_success(
    db_manager_mock: Mock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:

    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value={
            "name": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "email_verified": True,
            "is_admin": True,
            "team_id": None,
        }
    )

    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    assert isinstance(result, Ok)
    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.email_verified is True
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.is_admin is True
    assert result.ok_value.team_id is None


@pytest.mark.asyncio
async def test_update_participant_not_found(
    db_manager_mock: Mock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # When a participant with the specified id is not found find_one_and_update returns None
    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


# TODO: FIX
# @pytest.mark.asyncio
# async def test_fetch_all_success(
#     db_manager_mock: Mock,
#     repo: ParticipantsRepository,
#     mock_random_participant: Participant,
# ) -> None:
#     mock_participants_data = [
#         {
#             "_id": mock_random_participant.id,
#             "name": mock_random_participant.name,
#             "email": mock_random_participant.email,
#             "is_admin": mock_random_participant.is_admin,
#             "email_verified": mock_random_participant.email_verified,
#             "team_id": mock_random_participant.team_id,
#             "created_at": mock_random_participant.created_at,
#             "updated_at": mock_random_participant.updated_at,
#         }
#         for _ in range(5)
#     ]
#
#     db_manager_mock.get_collection.return_value.find = AsyncMock(return_value=mock_participants_data)
#
#     result = await repo.fetch_all()
#
#     assert isinstance(result, Ok)
#     assert len(result.ok_value) == 5
#
#     for i, participant in enumerate(result.ok_value):
#         assert participant.name == mock_participants_data[i]["name"]
#         assert participant.email == mock_participants_data[i]["email"]
#         assert participant.is_admin == mock_participants_data[i]["is_admin"]
#         assert participant.email_verified == mock_participants_data[i]["email_verified"]
#         assert participant.team_id == mock_participants_data[i]["team_id"]
#         assert participant.id == str(mock_participants_data[i]["_id"])
#
# @pytest.mark.asyncio
# async def test_fetch_all_empty(
#     db_manager_mock: Mock,
#     repo: ParticipantsRepository,
# ) -> None:
#     db_manager_mock.get_collection.return_value.find = AsyncMock(return_value=[])
#
#     result = await repo.fetch_all()
#
#     assert isinstance(result, Ok)
#     assert len(result.ok_value) == 0
#
# @pytest.mark.asyncio
# async def test_fetch_all_error(
#     db_manager_mock: Mock,
#     repo: ParticipantsRepository,
# ) -> None:
#     db_manager_mock.get_collection.return_value.find = AsyncMock(side_effect=Exception())
#
#     result = await repo.fetch_all()
#
#     assert isinstance(result, Err)
