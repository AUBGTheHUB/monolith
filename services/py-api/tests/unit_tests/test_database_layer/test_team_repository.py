from datetime import datetime
from typing import Tuple, cast, Dict, Any
from unittest.mock import Mock, AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err
from bson import ObjectId

from src.database.model.hackathon.team_model import Team, UpdateTeamParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import TeamNotFoundError, DuplicateTeamNameError
from tests.integration_tests.conftest import TEST_TEAM_NAME
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> TeamsRepository:
    return TeamsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_team_success(
    ten_sec_window: Tuple[datetime, datetime],
    unverified_team_mock: Team,
    repo: TeamsRepository,
) -> None:

    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(unverified_team_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.name == unverified_team_mock.name
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_team_duplicate_name_error(
    mongo_db_manager_mock: MongoDbManagerMock, unverified_team_mock: Team, repo: TeamsRepository
) -> None:

    # Given
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate team name
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate team name error")
    )

    # When
    result = await repo.create(unverified_team_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    # Check that the error message contains the team name
    assert str(result.err_value) == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_create_team_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, unverified_team_mock: Team, repo: TeamsRepository
) -> None:

    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(unverified_team_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_team_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    unverified_team_dump_no_id_mock: Dict[str, Any],
    obj_id_mock: str,
    repo: TeamsRepository,
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=unverified_team_dump_no_id_mock
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified is False


@pytest.mark.asyncio
async def test_delete_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: TeamsRepository
) -> None:

    # Given
    # When the team with the sepcified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: TeamsRepository
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
async def test_update_team_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    verified_team_dump_no_id_mock: Dict[str, Any],
    repo: TeamsRepository,
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=verified_team_dump_no_id_mock
    )

    # When
    result = await repo.update(obj_id_mock, UpdateTeamParams(is_verified=True))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.is_verified is True
    assert result.ok_value.name == TEST_TEAM_NAME


@pytest.mark.asyncio
async def test_update_team_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: TeamsRepository
) -> None:

    # Given
    # When a team with the specified id is not found find_one_and_update returns none
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateTeamParams(is_verified=True))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_success(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, unverified_team_mock: Team, repo: TeamsRepository
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(
        return_value=unverified_team_mock.dump_as_mongo_db_document()
    )

    # When
    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == obj_id_mock
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_team_name_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TeamsRepository
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_team_name_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TeamsRepository
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    result = await repo.fetch_by_team_name(TEST_TEAM_NAME)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    unverified_team_dump_no_id_mock: Dict[str, Any],
    repo: TeamsRepository,
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=unverified_team_dump_no_id_mock)

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Team)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.name == TEST_TEAM_NAME
    assert result.ok_value.is_verified == False


@pytest.mark.asyncio
async def test_fetch_by_id_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TeamsRepository, obj_id_mock: str
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TeamsRepository, obj_id_mock: str
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
    repo: TeamsRepository,
    verified_team_mock: Team,
) -> None:

    # Given
    mock_teams_data = [
        {
            "_id": verified_team_mock.id,
            "name": verified_team_mock.name,
            "is_verified": verified_team_mock.is_verified,
            "created_at": verified_team_mock.created_at,
            "updated_at": verified_team_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_teams_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, team in enumerate(result.ok_value):
        assert team.name == mock_teams_data[i]["name"]
        assert team.is_verified == mock_teams_data[i]["is_verified"]
        assert team.created_at == mock_teams_data[i]["created_at"]
        assert team.updated_at == mock_teams_data[i]["updated_at"]
        assert team.id == str(mock_teams_data[i]["id"])


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: TeamsRepository,
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
    repo: TeamsRepository,
) -> None:

    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
