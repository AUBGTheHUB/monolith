from datetime import datetime
from typing import Tuple
from unittest.mock import Mock, AsyncMock

from bson import ObjectId
import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_manager import TEAMS_COLLECTION
from src.database.repository.teams_repository import TeamsRepository
from src.server.exception import DuplicateTeamNameError, TeamNotFoundError
from src.database.model.team_model import Team, UpdatedTeam
from tests.integration_tests.conftest import TEST_TEAM_NAME


@pytest.fixture
def repo(db_manager_mock: Mock) -> TeamsRepository:
    return TeamsRepository(db_manager_mock, TEAMS_COLLECTION)


@pytest.mark.asyncio
async def test_create_team_success(
    ten_sec_window: Tuple[datetime, datetime],
    mock_normal_team: Team,
    repo: TeamsRepository,
) -> None:
    start_time, end_time = ten_sec_window

    result = await repo.create(mock_normal_team)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.name == mock_normal_team.name
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_team_duplicate_name_error(
    db_manager_mock: Mock, mock_normal_team: Team, repo: TeamsRepository
) -> None:
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate team name
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate team name error")
    )

    result = await repo.create(mock_normal_team)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    # Check that the error message contains the team name
    assert str(result.err_value) == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_create_team_general_exception(
    db_manager_mock: Mock, mock_normal_team: Team, repo: TeamsRepository
) -> None:
    # Simulate a general exception raised by insert_one
    db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.create(mock_normal_team)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_team_success(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:

    db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value={"name": TEST_TEAM_NAME, "is_verified": False}
    )

    result = await repo.delete(mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == mock_obj_id
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
async def test_update_team_success(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value={"name": TEST_TEAM_NAME, "is_verified": True}
    )

    result = await repo.update(mock_obj_id, UpdatedTeam(is_verified=True))

    assert isinstance(result, Ok)
    assert result.ok_value.id == mock_obj_id
    assert result.ok_value.is_verified is True
    assert result.ok_value.name == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_update_team_team_not_found(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    # When a team with the specified id is not found find_one_and_update returns none
    db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    result = await repo.update(mock_obj_id, UpdatedTeam(is_verified=True))

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_success(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(
        return_value={"_id": ObjectId(mock_obj_id), "name": TEST_TEAM_NAME, "is_verified": False}
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
async def test_fetch_by_id_successful(db_manager_mock: Mock, mock_obj_id: str, repo: TeamsRepository) -> None:
    db_manager_mock.get_collection.return_value.find_one = AsyncMock(
        return_value={"name": TEST_TEAM_NAME, "is_verified": False}
    )

    result = await repo.fetch_by_id(mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)

    assert result.ok_value.id == mock_obj_id
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
