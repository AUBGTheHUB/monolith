from unittest.mock import AsyncMock

import pytest
from datetime import datetime
from typing import cast, Any
from pymongo.errors import DuplicateKeyError
from result import Ok, Err
from bson import ObjectId

from src.database.model.tournament_registration.tournament_participant_model import (
    TournamentParticipant,
    UpdateTournamentParticipantParams,
)
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.tournament.tournament_participants_repository import TournamentParticipantsRepository
from src.exception import DuplicateTournamentParticipantError, TournamentParticipantNotFoundError

from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import MongoDbManagerMock, MongoDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> TournamentParticipantsRepository:
    return TournamentParticipantsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_tour_participant_success(
    ten_sec_window: tuple[datetime, datetime],
    tournament_participant_mock: TournamentParticipant,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(tournament_participant_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentParticipant)
    assert result.ok_value.full_name == tournament_participant_mock.full_name
    assert result.ok_value.email == tournament_participant_mock.email
    assert result.ok_value.alternative_role is tournament_participant_mock.alternative_role
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_tour_participant_duplicate_email_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    tournament_participant_mock: TournamentParticipant,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate email
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate email error")
    )

    # When
    result = await repo.create(tournament_participant_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTournamentParticipantError)


@pytest.mark.asyncio
async def test_create_tour_participant_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock,
    tournament_participant_mock: TournamentParticipant,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(tournament_participant_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_tour_participant_successful(
    obj_id_mock: str,
    mongo_db_manager_mock: MongoDbManagerMock,
    tournament_participant_dict_mock: dict[str, Any],
    repo: TournamentParticipantsRepository,
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=tournament_participant_dict_mock
    )
    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentParticipant)
    assert result.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_tour_participant_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TournamentParticipantsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentParticipantNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: TournamentParticipantsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=Exception())

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_update_participant_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentParticipantsRepository,
    tournament_participant_mock: TournamentParticipant,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=tournament_participant_mock
    )

    # When
    result = await repo.update(obj_id_mock, UpdateTournamentParticipantParams(is_confirmed=True))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.is_confirmed is False
    assert result.ok_value.full_name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_update_participant_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: TournamentParticipantsRepository
) -> None:
    # Given
    # When a participant with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateTournamentParticipantParams(is_confirmed=True))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentParticipantNotFoundError)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: TournamentParticipantsRepository,
    tournament_participant_mock: TournamentParticipant,
) -> None:
    # Given
    # Prepare mock MongoDB documents
    mock_tournament_participants_data = [tournament_participant_mock.dump_as_mongo_db_document() for _ in range(5)]
    db_cursor_mock.to_list.return_value = mock_tournament_participants_data
    # Patch find() to return the mock cursor
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    # Run the method
    result = await repo.fetch_all()

    # Then
    # Assertions
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, participant in enumerate(result.ok_value):
        assert participant.full_name == mock_tournament_participants_data[i]["full_name"]
        assert participant.email == mock_tournament_participants_data[i]["email"]
        assert participant.is_confirmed == mock_tournament_participants_data[i]["is_confirmed"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MongoDbCursorMock,
    repo: TournamentParticipantsRepository,
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
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_fetch_by_id_tournament_participant_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    tournament_participant_mock: TournamentParticipant,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=tournament_participant_mock)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentParticipant)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.full_name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_fetch_by_id_not_found(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TournamentParticipantNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentParticipantsRepository,
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
async def test_find_by_email_tournament_participant_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    tournament_participant_mock: TournamentParticipant,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=tournament_participant_mock)

    # When
    result = await repo.find_by_email(email=TEST_USER_EMAIL)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, TournamentParticipant)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.full_name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_find_by_email_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(side_effect=Exception("General Error"))

    # When
    result = await repo.find_by_email(email=TEST_USER_EMAIL)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_check_team_members_count_by_team_id_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.count_documents = AsyncMock(return_value=5)

    # When
    result = await repo.check_team_members_count_by_team_id(team_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, int)
    assert result.ok_value == 5


@pytest.mark.asyncio
async def test_check_team_members_count_by_team_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: TournamentParticipantsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.count_documents = AsyncMock(
        side_effect=Exception("General Error")
    )

    # When
    result = await repo.check_team_members_count_by_team_id(team_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"
