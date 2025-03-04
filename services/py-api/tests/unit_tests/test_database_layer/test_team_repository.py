from datetime import datetime
from typing import Tuple, Dict, Any
from unittest.mock import Mock, AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err
from bson import ObjectId

from src.database.db_manager import TEAMS_COLLECTION
from src.database.repository.teams_repository import TeamsRepository
from src.server.exception import DuplicateTeamNameError, TeamNotFoundError
from src.database.model.team_model import Team, UpdateTeamParams
from tests.integration_tests.conftest import TEST_TEAM_NAME


@pytest.fixture
def repo(db_manager_mock: Mock) -> TeamsRepository:
    return TeamsRepository(db_manager_mock, TEAMS_COLLECTION)


@pytest.mark.asyncio
async def test_create_team_success(
    ten_sec_window: Tuple[datetime, datetime],
    mock_unverified_team: Team,
    repo: TeamsRepository,
) -> None:
    start_time, end_time = ten_sec_window

    result = await repo.create(mock_unverified_team)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.name == mock_unverified_team.name
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_team_duplicate_name_error(
    db_manager_mock: Mock, mock_unverified_team: Team, repo: TeamsRepository
) -> None:
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate team name
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate team name error")
    )

    result = await repo.create(mock_unverified_team)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    # Check that the error message contains the team name
    assert str(result.err_value) == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_create_team_general_exception(
    db_manager_mock: Mock, mock_unverified_team: Team, repo: TeamsRepository
) -> None:
    # Simulate a general exception raised by insert_one
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.create(mock_unverified_team)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_team_success(
    db_manager_mock: Mock, mock_unverified_team_dump_no_id: Dict[str, Any], mock_obj_id: str, repo: TeamsRepository
) -> None:

    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=mock_unverified_team_dump_no_id
    )

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == ObjectId(mock_obj_id)
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified is False


@pytest.mark.asyncio
async def test_delete_team_not_found(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:

    # When the team with the sepcified object id is not found find_one_and_delete returns None
    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_delete_team_general_exception(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    # Simulate a general exception raised by insert_one
    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_update_team_success(
    db_manager_mock: Mock, mock_obj_id: str, mock_verified_team_dump_no_id: Dict[str, Any], repo: TeamsRepository
) -> None:
    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=mock_verified_team_dump_no_id
    )

    result = await repo.update(mock_obj_id, UpdateTeamParams(is_verified=True))

    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(mock_obj_id)
    assert result.ok_value.is_verified is True
    assert result.ok_value.name == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_update_team_team_not_found(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    # When a team with the specified id is not found find_one_and_update returns none
    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    result = await repo.update(mock_obj_id, UpdateTeamParams(is_verified=True))

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_success(
    db_manager_mock: Mock, mock_obj_id: str, mock_unverified_team: Team, repo: TeamsRepository
) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(
        return_value=mock_unverified_team.dump_as_mongo_db_document()
    )

    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)

    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_team_name_team_not_found(db_manager_mock: Mock, repo: TeamsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_general_error(db_manager_mock: Mock, repo: TeamsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    db_manager_mock: Mock, mock_obj_id: str, mock_unverified_team_dump_no_id: Dict[str, Any], repo: TeamsRepository
) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=mock_unverified_team_dump_no_id)

    result = await repo.fetch_by_id(mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)

    assert result.ok_value.id == ObjectId(mock_obj_id)
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_id_team_not_found(db_manager_mock: Mock, repo: TeamsRepository, mock_obj_id: str) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    result = await repo.fetch_by_id(mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(db_manager_mock: Mock, repo: TeamsRepository, mock_obj_id: str) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    result = await repo.fetch_by_id(mock_obj_id)

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
