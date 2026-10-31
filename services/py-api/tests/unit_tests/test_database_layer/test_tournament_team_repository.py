from datetime import datetime
from typing import cast, Any
from unittest.mock import AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err
from bson import ObjectId

from src.database.model.tournament_registration.tournament_team_model import TournamentTeam, UpdateTournamentTeamParams
from src.database.mongo.db_manager import MongoDatabaseManager

from src.database.repository.tournament.tournament_teams_repository import TournamentTeamsRepository
from src.exception import DuplicateTournamentTeamNameError, TournamentTeamNotFoundError
from tests.integration_tests.conftest import TEST_TEAM_CODE
from tests.unit_tests.conftest import MongoDbManagerMock, MongoDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> TournamentTeamsRepository:
    return TournamentTeamsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_tour_team_success(
    ten_sec_window: tuple[datetime, datetime],
    tournament_team_mock: TournamentTeam,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(tournament_team_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentTeam)
    assert result.ok_value.code == tournament_team_mock.code
    assert result.ok_value.name == tournament_team_mock.name
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_tour_team_duplicate_name_error(
    mongo_db_manager_mock: MongoDbManagerMock, tournament_team_mock: TournamentTeam, repo: TournamentTeamsRepository
) -> None:
    # Given
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate name
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate team name error")
    )

    # When
    result = await repo.create(tournament_team_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTournamentTeamNameError)


@pytest.mark.asyncio
async def test_create_tour_team_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, tournament_team_mock: TournamentTeam, repo: TournamentTeamsRepository
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(tournament_team_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_tour_team_successful(
    obj_id_mock: str,
    mongo_db_manager_mock: MongoDbManagerMock,
    tournament_team_dict_mock: dict[str, Any],
    repo: TournamentTeamsRepository,
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=tournament_team_dict_mock
    )
    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentTeam)
    assert result.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_tour_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TournamentTeamsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentTeamNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TournamentTeamsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=Exception())

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_team_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentTeamsRepository,
    tournament_team_mock: TournamentTeam,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=tournament_team_mock)

    # When
    result = await repo.update(obj_id_mock, UpdateTournamentTeamParams(code=TEST_TEAM_CODE))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.code is TEST_TEAM_CODE


@pytest.mark.asyncio
async def test_update_team_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: TournamentTeamsRepository
) -> None:
    # Given
    # When a participant with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateTournamentTeamParams(code=TEST_TEAM_CODE))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentTeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: TournamentTeamsRepository,
    tournament_team_mock: TournamentTeam,
) -> None:
    # Given
    # Prepare mock MongoDB documents
    mock_tour_team_data = [tournament_team_mock.dump_as_mongo_db_document() for _ in range(5)]
    db_cursor_mock.to_list.return_value = mock_tour_team_data
    # Patch find() to return the mock cursor
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    # Run the method
    result = await repo.fetch_all()

    # Then
    # Assertions
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, team in enumerate(result.ok_value):
        assert team.code == mock_tour_team_data[i]["code"]
        assert team.name == mock_tour_team_data[i]["name"]
        assert team.id == ObjectId(mock_tour_team_data[i]["id"])


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: TournamentTeamsRepository,
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
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_fetch_by_id_tournament_team_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    tournament_team_mock: TournamentTeam,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=tournament_team_mock)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentTeam)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.code == TEST_TEAM_CODE


@pytest.mark.asyncio
async def test_fetch_by_id_not_found(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentTeamNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(side_effect=Exception("General Error"))

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_find_by_code_tournament_team_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    tournament_team_mock: TournamentTeam,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(
        return_value=tournament_team_mock.dump_as_mongo_db_document()
    )

    # When
    result = await repo.find_by_code(code=TEST_TEAM_CODE)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentTeam)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.code == TEST_TEAM_CODE


@pytest.mark.asyncio
async def test_find_by_code_not_found(
    mongo_db_manager_mock: MongoDbManagerMock,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.find_by_code(code=TEST_TEAM_CODE)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentTeamNotFoundError)


@pytest.mark.asyncio
async def test_find_by_code_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    repo: TournamentTeamsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(side_effect=Exception("General Error"))

    # When
    result = await repo.find_by_code(code=TEST_TEAM_CODE)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"
