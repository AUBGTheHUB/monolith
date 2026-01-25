from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.exception import SponsorNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock
from structlog.stdlib import get_logger


def _validate_fields(expected: Sponsor, actual: Sponsor) -> bool:
    return (
        str(actual.id) == str(expected.id)
        and actual.name == expected.name
        and actual.tier == expected.tier
        and actual.website_url == expected.website_url
        and actual.logo_url == expected.logo_url
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> SponsorsRepository:
    return SponsorsRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))

@pytest.mark.asyncio
async def test_create_sponsor_success(
    ten_sec_window: tuple[datetime, datetime],
    sponsor_mock: Sponsor,
    repo: SponsorsRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    response = await repo.create(sponsor_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Sponsor)
    assert _validate_fields(response.ok_value, sponsor_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= response.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= response.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_sponsor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, sponsor_mock: Sponsor, repo: SponsorsRepository
) -> None:
    # Given
    # Create a mock exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    response = await repo.create(sponsor_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the one in the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_sponsor_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    sponsor_mock: dict[str, Any],
    obj_id_mock: str,
    repo: SponsorsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=sponsor_mock
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Sponsor)
    assert response.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_sponsor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: SponsorsRepository
) -> None:
    # Given
    # When the past event with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, SponsorNotFoundError)


@pytest.mark.asyncio
async def test_delete_sponsor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: SponsorsRepository
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the same as the mock
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_update_sponsor_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    sponsor_no_id_mock: dict[str, Any],
    repo: SponsorsRepository,
) -> None:
    # Given
    sponsor_no_id_mock["name"] = "Coca-Cola HBC"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=sponsor_no_id_mock
    )

    # When
    response = await repo.update(obj_id_mock, UpdateSponsorParams(name="Coca-Cola HBC"))

    # Then
    assert isinstance(response, Ok)
    assert response.ok_value.id == ObjectId(obj_id_mock)
    assert response.ok_value.name == "Coca-Cola HBC"


@pytest.mark.asyncio
async def test_update_sponsor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: SponsorsRepository
) -> None:
    # Given
    # When a sponsor with the specified id is not found find_one_and_update returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    response = await repo.update(obj_id_mock, UpdateSponsorParams(name="Coca-Cola HBC"))

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, SponsorNotFoundError)


@pytest.mark.asyncio
async def test_update_sponsor_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: SponsorsRepository, obj_id_mock: str
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    response = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(response.err_value) == "Test error"


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    sponsor_no_id_mock: dict[str, Any],
    sponsor_mock: Sponsor,
    repo: SponsorsRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=sponsor_no_id_mock)

    # When
    response = await repo.fetch_by_id(str(sponsor_mock.id))

    # Then
    assert isinstance(response, Ok)
    assert isinstance(response.ok_value, Sponsor)
    assert _validate_fields(sponsor_mock, response.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_sponsor_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: SponsorsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, SponsorNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: SponsorsRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=Exception("Test Error"))

    # When
    response = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(response, Err)
    assert isinstance(response.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: SponsorsRepository,
    sponsor_mock: Sponsor,
) -> None:
    # Given
    mock_sponsors_data = [
        {
            "_id": sponsor_mock.id,
            "name": sponsor_mock.name,
            "tier": sponsor_mock.tier,
            "website_url": sponsor_mock.website_url,
            "logo_url": sponsor_mock.logo_url,
            "created_at": sponsor_mock.created_at,
            "updated_at": sponsor_mock.updated_at,
        }
        for _ in range(5) # ????
    ]
    db_cursor_mock.to_list.return_value = mock_sponsors_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 5

    for i, sponsor in enumerate(response.ok_value):
        assert sponsor.name == mock_sponsors_data[i]["name"]
        assert sponsor.tier == mock_sponsors_data[i]["tier"]
        assert sponsor.website_url == mock_sponsors_data[i]["website_url"]
        assert sponsor.logo_url == mock_sponsors_data[i]["logo_url"]
        assert sponsor.created_at == mock_sponsors_data[i]["created_at"]
        assert sponsor.updated_at == mock_sponsors_data[i]["updated_at"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: SponsorsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = []
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Ok)
    assert len(response.ok_value) == 0


@pytest.mark.asyncio
async def test_fetch_all_error(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: SponsorsRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.return_value = Exception()
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    response = await repo.fetch_all()

    # Then
    assert isinstance(response, Err)
