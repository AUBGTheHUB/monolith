from datetime import datetime
from typing import Tuple, cast

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_managers import TEAMS_COLLECTION_NAME, MongoDatabaseManager
from src.database.repository.teams_repository import TeamsRepository
from src.server.exception import DuplicateTeamNameError, TeamNotFoundError
from src.database.model.team_model import Team, UpdateTeamParams
from tests.integration_tests.conftest import TEST_TEAM_NAME
from tests.unit_tests.conftest import MongoDbManagerMock, MotorCollectionMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> TeamsRepository:
    return TeamsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock), TEAMS_COLLECTION_NAME)


@pytest.mark.asyncio
async def test_create_team_success(
    five_sec_window: Tuple[datetime, datetime],
    mock_normal_team: Team,
    repo: TeamsRepository,
) -> None:
    # Given some five seconds window for assessing timestamps of created_at and updated_at fields
    # And no errors from Mongo
    start_time, end_time = five_sec_window

    # When we create a Team document in Mongo
    result = await repo.create(mock_normal_team)

    # Then the creation of the team should succeed within this five seconds window
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.name == mock_normal_team.name
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_team_duplicate_name_error(
    motor_collection_mock: MotorCollectionMock, mock_normal_team: Team, repo: TeamsRepository
) -> None:
    # Given a DuplicateKeyError raised by insert_one, due to a duplicate team name in the collection
    motor_collection_mock.insert_one.side_effect = DuplicateKeyError("Duplicate team name error")

    # When we create a Team document in Mongo
    result = await repo.create(mock_normal_team)

    # Then the creation of the team should fail, and we should get an Err(DuplicateTeamNameError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    # Check that the error message contains the team name
    assert str(result.err_value) == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_create_team_general_exception(
    motor_collection_mock: MotorCollectionMock, mock_normal_team: Team, repo: TeamsRepository
) -> None:
    # Given a general exception raised by insert_one
    motor_collection_mock.insert_one.side_effect = Exception("Test error")

    # When we create a Team document in Mongo
    result = await repo.create(mock_normal_team)

    # Then the creation of the team should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_delete_team_success(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a successful response by find_one_and_delete (this is the Team obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one_and_delete.return_value = {"name": TEST_TEAM_NAME, "is_verified": False}

    # When we delete a Team document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should succeed, and the deleted Team object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified is False


@pytest.mark.asyncio
async def test_delete_team_not_found(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a None response by find_one_and_delete, indicating the Team we are trying to delete is not found
    motor_collection_mock.find_one_and_delete.return_value = None

    # When we delete a Team document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should fail, and we should get an Err(TeamNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a general exception raised by find_one_and_delete
    motor_collection_mock.find_one_and_delete.side_effect = Exception("Test error")

    # When we delete a Team document in Mongo
    result = await repo.delete(mock_obj_id)

    # Then the deletion should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_team_success(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a successful response by find_one_and_update (this is the Team obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one_and_update.return_value = {"name": TEST_TEAM_NAME, "is_verified": True}

    # When we update the Team document in Mongo
    result = await repo.update(mock_obj_id, UpdateTeamParams(is_verified=True))

    # Then the update should succeed, and the updated Team object should be returned.
    assert isinstance(result, Ok)
    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.is_verified is True
    assert result.ok_value.name == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_update_team_team_not_found(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a None response by find_one_and_delete, indicating the Team we are trying to delete is not found
    motor_collection_mock.find_one_and_update.return_value = None

    # When we update the Team document in Mongo
    result = await repo.update(mock_obj_id, UpdateTeamParams(is_verified=True))

    # Then the update should fail, and we should get an Err(TeamNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_update_team_general_error(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a general exception raised by find_one_and_update
    motor_collection_mock.find_one_and_update.side_effect = Exception("Test error")

    # When we update the Team document in Mongo
    result = await repo.update(mock_obj_id, UpdateTeamParams(is_verified=True))

    # Then the update should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_by_team_name_success(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a successful response by find_one
    motor_collection_mock.find_one.return_value = {
        "_id": mock_obj_id,
        "name": TEST_TEAM_NAME,
        "is_verified": False,
    }

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    # Then the fetch should succeed, and the Team object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_team_name_team_not_found(
    motor_collection_mock: MotorCollectionMock, repo: TeamsRepository
) -> None:
    # Given a None response by find_one, indicating the Team we are trying to fetch is not found
    motor_collection_mock.find_one.return_value = None

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    # Then the fetch should fail, and we should get an Err(TeamNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_general_error(
    motor_collection_mock: MotorCollectionMock, repo: TeamsRepository
) -> None:
    # Given a general exception raised by find_one
    motor_collection_mock.find_one.side_effect = Exception("Test Error")

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    # Then the fetch should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    motor_collection_mock: MotorCollectionMock, mock_obj_id: str, repo: TeamsRepository
) -> None:
    # Given a successful response by find_one (this is the Team obj json representation without the
    # "_id" property as it is projected (omitted from the response), you can check the method for more info)
    motor_collection_mock.find_one.return_value = {"name": TEST_TEAM_NAME, "is_verified": False}

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the update should succeed, and the updated Team object should be returned.
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_id_team_not_found(
    motor_collection_mock: MotorCollectionMock, repo: TeamsRepository, mock_obj_id: str
) -> None:
    # Given a None response by find_one, indicating the Team we are trying to fetch is not found
    motor_collection_mock.find_one.return_value = None

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the fetch should fail, and we should get an Err(TeamNotFoundError())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    motor_collection_mock: MotorCollectionMock, repo: TeamsRepository, mock_obj_id: str
) -> None:
    # Given a general exception raised by find_one
    motor_collection_mock.find_one.side_effect = Exception("Test Error")

    # When we fetch the Team document in Mongo
    result = await repo.fetch_by_id(mock_obj_id)

    # Then the fetch should fail, and we should get an Err(Exception())
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


# TODO: FIX
# @pytest.mark.asyncio
# async def test_fetch_all_success(
#     db_manager_mock: Mock,
#     repo: TeamsRepository,
#     mock_normal_team: Team,
# ) -> None:
#     mock_teams_data = [
#         {
#             "_id": mock_normal_team.id,
#             "name": mock_normal_team.name,
#             "is_verified": mock_normal_team.is_verified,
#             "created_at": mock_normal_team.created_at,
#             "updated_at": mock_normal_team.updated_at,
#         }
#         for _ in range(5)
#     ]
#
#     db_manager_mock.get_collection.return_value.find = AsyncMock(return_value=mock_teams_data)
#
#     result = await repo.fetch_all()
#
#     assert isinstance(result, Ok)
#     assert len(result.ok_value) == 5
#
#     for i, team in enumerate(result.ok_value):
#         assert team.name == mock_teams_data[i]["name"]
#         assert team.is_verified == mock_teams_data[i]["is_verified"]
#         assert team.created_at == mock_teams_data[i]["created_at"]
#         assert team.updated_at == mock_teams_data[i]["updated_at"]
#         assert team.id == str(mock_teams_data[i]["_id"])
#
# @pytest.mark.asyncio
# async def test_fetch_all_empty(
#     db_manager_mock: Mock,
#     repo: TeamsRepository,
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
#     repo: TeamsRepository,
# ) -> None:
#     db_manager_mock.get_collection.return_value.find = AsyncMock(side_effect=Exception("Database error"))
#
#     result = await repo.fetch_all()
#
#     assert isinstance(result, Err)
#     assert str(result.err_value) == "Database error"
