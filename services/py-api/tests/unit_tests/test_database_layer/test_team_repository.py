from datetime import datetime
from typing import Tuple
from unittest.mock import Mock, AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_manager import TEAMS_COLLECTION
from src.database.repository.teams_repository import TeamsRepository
from src.server.exception import DuplicateTeamNameError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.database.model.team_model import Team


@pytest.fixture
def repo(db_manager_mock: Mock) -> TeamsRepository:
    return TeamsRepository(db_manager_mock, TEAMS_COLLECTION)


@pytest.mark.asyncio
async def test_create_team_success(
    db_manager_mock: Mock,
    ten_sec_window: Tuple[datetime, datetime],
    mock_input_data: ParticipantRequestBody,
    repo: TeamsRepository,
) -> None:
    start_time, end_time = ten_sec_window

    team = Team(name=mock_input_data.team_name)
    team_document = team.dump_as_mongo_db_document()

    # Mock insert_one to simulate successful insertion
    repo._collection.insert_one = AsyncMock()

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    # We cannot use assert_awaited_once_with(document=team_document, session=None) because it would require
    # an exact match between the passed document in the test and the actual document created dynamically within
    # `repo.create(input_data)`. Since fields like `_id`, `created_at`, and `updated_at` are generated one demand each
    # time `Team` is  instantiated, the values in the team_document above will differ from the once
    # in the actual document created dynamically within `repo.create(input_data), making an exact match impossible.
    # That's why we are comparing only certain fields from the passed document.
    actual_call_args = repo._collection.insert_one.call_args[1]["document"]

    assert actual_call_args["name"] == team_document["name"]

    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= actual_call_args["created_at"] <= end_time, "created_at is not within the 10-second window"
    assert start_time <= actual_call_args["updated_at"] <= end_time, "updated_at is not within the 10-second window"

    # Assert the result is Ok
    assert isinstance(result, Ok)
    assert result.ok_value.name == mock_input_data.team_name


@pytest.mark.asyncio
async def test_create_team_duplicate_name_error(
    db_manager_mock: Mock, mock_input_data: ParticipantRequestBody, repo: TeamsRepository
) -> None:
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate team name
    repo._collection.insert_one = AsyncMock(side_effect=DuplicateKeyError("Duplicate team name error"))

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    # Check that the error message contains the team name
    assert str(result.err_value) == "Test Team"


@pytest.mark.asyncio
async def test_create_team_general_exception(
    db_manager_mock: Mock, mock_input_data: ParticipantRequestBody, repo: TeamsRepository
) -> None:
    # Simulate a general exception raised by insert_one
    repo._collection.insert_one = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"
