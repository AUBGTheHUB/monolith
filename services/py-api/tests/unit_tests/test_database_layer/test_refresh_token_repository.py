from datetime import datetime
from typing import cast, Any
from unittest.mock import AsyncMock

import pytest
from result import Ok, Err

from src.database.model.admin.refresh_token import RefreshToken, UpdateRefreshTokenParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import RefreshTokenNotFound
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> RefreshTokenRepository:
    return RefreshTokenRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_refresh_token_success(
    ten_sec_window: tuple[datetime, datetime],
    refresh_token_mock: RefreshToken,
    repo: RefreshTokenRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(refresh_token_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, RefreshToken)

    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_refresh_token_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock,
    refresh_token_mock: RefreshToken,
    repo: RefreshTokenRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(refresh_token_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_refresh_token_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    refresh_token_dict_mock: dict[str, Any],
    repo: RefreshTokenRepository,
) -> None:
    # Given

    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=refresh_token_dict_mock
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, RefreshToken)
    assert result.ok_value.id == obj_id_mock


@pytest.mark.asyncio
async def test_delete_refresh_token_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: RefreshTokenRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RefreshTokenNotFound)


@pytest.mark.asyncio
async def test_delete_refresh_token_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: RefreshTokenRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_update_refresh_token_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: RefreshTokenRepository,
    refresh_token_dict_mock: dict[str, Any],
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=refresh_token_dict_mock
    )

    # When
    result = await repo.update(obj_id_mock, UpdateRefreshTokenParams(hub_member_id=obj_id_mock))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == obj_id_mock


@pytest.mark.asyncio
async def test_update_refresh_token_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: RefreshTokenRepository
) -> None:
    # Given
    # When a participant with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateRefreshTokenParams(hub_member_id=obj_id_mock))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RefreshTokenNotFound)


import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_fetch_all_refresh_tokens_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: RefreshTokenRepository,
    refresh_token_dict_mock: dict[str, Any],
) -> None:
    # Given
    mock_refresh_tokens_data = [refresh_token_dict_mock for _ in range(5)]
    db_cursor_mock.to_list.return_value = mock_refresh_tokens_data
    # Patch find() to return the mock cursor
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    # Run the method
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, refresh_token in enumerate(result.ok_value):
        assert refresh_token["id"] == str(mock_refresh_tokens_data[i]["_id"])


@pytest.mark.asyncio
async def test_fetch_all_refresh_tokens_empty(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: RefreshTokenRepository,
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
async def test_fetch_all_refresh_tokens_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: RefreshTokenRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
