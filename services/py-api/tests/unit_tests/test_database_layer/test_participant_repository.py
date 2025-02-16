from datetime import datetime
from typing import Tuple, cast

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_managers import PARTICIPANTS_COLLECTION_NAME, MongoDatabaseManager
from src.database.model.participant_model import Participant, UpdateParticipantParams
from src.database.repository.participants_repository import ParticipantsRepository
from src.server.exception import DuplicateEmailError, ParticipantNotFoundError
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME
from unit_tests.conftest import MongoDbManagerMock, MotorCollectionMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> ParticipantsRepository:
    return ParticipantsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock), PARTICIPANTS_COLLECTION_NAME)


@pytest.mark.asyncio
async def test_create_participant_success(
    five_sec_window: Tuple[datetime, datetime],
    mock_random_participant: Participant,
    repo: ParticipantsRepository,
) -> None:
    # Given some five seconds window for assessing timestamps of created_at and updated_at fields
    # And no errors from Mongo
    start_time, end_time = five_sec_window

    # When we create a Participant document in Mongo
    result = await repo.create(mock_random_participant)

    # Then the creation of the participant should succeed within this five seconds window
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
    motor_collection_mock: MotorCollectionMock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:
    # Given a DuplicateKeyError raised by insert_one, due to a duplicate email in the collection
    motor_collection_mock.insert_one.side_effect = DuplicateKeyError("Duplicate email error")

    # When we create a Participant document in Mongo
    result = await repo.create(mock_random_participant)

    # Then the creation of the participant should fail, and we should get an Err(DuplicateEmailError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    # Check that the error message is the duplicate email as expected
    assert str(result.err_value) == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_create_participant_general_exception(
    motor_collection_mock: MotorCollectionMock, mock_random_participant: Participant, repo: ParticipantsRepository
) -> None:
    # Given a general exception raised by insert_one
    motor_collection_mock.insert_one.side_effect = Exception("Test error")

    # When we create a Participant document in Mongo
    result = await repo.create(mock_random_participant)

    # Then the creation of the participant should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_delete_successful(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # Given a successful response by find_one_and_delete (this is the Participant obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one_and_delete.return_value = {
        "name": TEST_USER_NAME,
        "email": TEST_USER_EMAIL,
        "is_admin": False,
        "email_verified": False,
        "team_id": mock_obj_id,
    }

    # When we delete the Participant document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should succeed, and the deleted Participant object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.email_verified == False


@pytest.mark.asyncio
async def test_delete_participant_not_found(
    motor_collection_mock: MotorCollectionMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:
    # Given a None response by find_one_and_delete, indicating the Participant we are trying to delete is not found
    motor_collection_mock.find_one_and_delete.return_value = None

    # When we delete the Participant document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should fail, and we should get an Err(ParticipantNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(
    motor_collection_mock: MotorCollectionMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:
    # Given a general exception raised by find_one_and_delete
    motor_collection_mock.find_one_and_delete.side_effect = Exception("Test error")

    # When we delete the Participant document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_participant_success(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # Given a successful response by find_one_and_update (this is the Participant obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one_and_update.return_value = {
        "name": TEST_USER_NAME,
        "email": TEST_USER_EMAIL,
        "email_verified": True,
        "is_admin": True,
        "team_id": None,
    }

    # When we update the Participant document in Mongo
    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    # Then the update should succeed, and the updated Participant object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.email_verified is True
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.is_admin is True
    assert result.ok_value.team_id is None


@pytest.mark.asyncio
async def test_update_participant_not_found(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # Given a None response by find_one_and_delete, indicating the Participant we are trying to delete is not found
    motor_collection_mock.find_one_and_update.return_value = None

    # When we update the Participant document in Mongo
    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    # Then the update should fail, and we should get an Err(ParticipantNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_update_participant_general_error(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # Given a general exception raised by find_one_and_update
    motor_collection_mock.find_one_and_update.side_effect = Exception("Test error")

    # When we update the Participant document in Mongo
    result = await repo.update(mock_obj_id, UpdateParticipantParams(email_verified=True))

    # Then the update should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: ParticipantsRepository
) -> None:
    # Given a successful response by find_one (this is the Participant obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one.return_value = {
        "name": TEST_USER_NAME,
        "email": TEST_USER_EMAIL,
        "is_admin": True,
        "email_verified": False,
        "team_id": mock_obj_id,
    }

    # When we fetch the Participant document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the update should succeed, and the updated Participant object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL
    assert result.ok_value.is_admin is True
    assert result.ok_value.email_verified is False
    assert result.ok_value.team_id == mock_obj_id


@pytest.mark.asyncio
async def test_fetch_by_id_participant_not_found(
    motor_collection_mock: MotorCollectionMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:
    # Given a None response by find_one, indicating the Participant we are trying to fetch is not found
    motor_collection_mock.find_one.return_value = None

    # When we fetch the Participant document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the fetch should fail, and we should get an Err(ParticipantNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    motor_collection_mock: MotorCollectionMock, repo: ParticipantsRepository, mock_obj_id: str
) -> None:
    # Given a general exception raised by find_one
    motor_collection_mock.find_one.side_effect = Exception("Test Error")

    # When we fetch the Participant document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the fetch should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


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
