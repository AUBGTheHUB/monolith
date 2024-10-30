from datetime import datetime
from typing import Tuple
from unittest.mock import Mock, AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.db_manager import PARTICIPANTS_COLLECTION
from src.database.model.participant_model import Participant
from src.database.repository.participants_repository import ParticipantsRepository
from src.server.exception import DuplicateEmailError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody


@pytest.fixture
def repo(db_manager_mock: Mock) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager_mock, PARTICIPANTS_COLLECTION)


@pytest.mark.asyncio
async def test_create_participant_success(
    db_manager_mock: Mock,
    ten_sec_window: Tuple[datetime, datetime],
    mock_input_data: ParticipantRequestBody,
    repo: ParticipantsRepository,
) -> None:
    start_time, end_time = ten_sec_window

    participant = Participant(
        name=mock_input_data.name,
        email=mock_input_data.email,
        is_admin=mock_input_data.is_admin,
        email_verified=False,  # default value as per the model definition
        team_id=None,
    )
    participant_document = participant.dump_as_mongo_db_document()

    # By using AsyncMock, we’re simulating the behavior of insert_one as if it succeeded without making an actual
    # database call
    repo._collection.insert_one = AsyncMock()

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    # We cannot use assert_awaited_once_with(document=participant_document, session=None) because it would require
    # an exact match between the passed document in the test and the actual document created dynamically within
    # `repo.create(input_data)`. Since fields like `_id`, `created_at`, and `updated_at` are generated one demand each
    # time `Participant` is  instantiated, the values in the participant_document above will differ from the once
    # in the actual document created dynamically within `repo.create(input_data), making an exact match impossible.
    # That's why we are comparing only certain fields from the passed document.
    actual_call_args = repo._collection.insert_one.call_args[1]["document"]

    # Validate each field except _id and timestamps directly
    assert actual_call_args["name"] == participant_document["name"]
    assert actual_call_args["email"] == participant_document["email"]
    assert actual_call_args["is_admin"] == participant_document["is_admin"]
    assert actual_call_args["email_verified"] == participant_document["email_verified"]
    assert actual_call_args["team_id"] == participant_document["team_id"]

    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= actual_call_args["created_at"] <= end_time, "created_at is not within the 10-second window"
    assert start_time <= actual_call_args["updated_at"] <= end_time, "updated_at is not within the 10-second window"

    assert isinstance(result, Ok)


@pytest.mark.asyncio
async def test_create_participant_duplicate_email_error(
    db_manager_mock: Mock, mock_input_data: ParticipantRequestBody, repo: ParticipantsRepository
) -> None:
    # Simulate a DuplicateKeyError raised by insert_one to represent a duplicate email
    repo._collection.insert_one = AsyncMock(side_effect=DuplicateKeyError("Duplicate email error"))

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    # Assert the result is an Err containing DuplicateEmailError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    # Check that the error message is the duplicate email as expected
    assert str(result.err_value) == "test@example.com"


@pytest.mark.asyncio
async def test_create_participant_general_exception(
    db_manager_mock: Mock, mock_input_data: ParticipantRequestBody, repo: ParticipantsRepository
) -> None:
    # Simulate a general exception raised by insert_one
    repo._collection.insert_one = AsyncMock(side_effect=Exception("Test error"))

    result = await repo.create(mock_input_data)

    # Check that insert_one was awaited once
    repo._collection.insert_one.assert_awaited_once()

    # Assert the result is an Err containing DuplicateEmailError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"
