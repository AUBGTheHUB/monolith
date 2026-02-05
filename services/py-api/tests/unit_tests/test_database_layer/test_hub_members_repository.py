from unittest.mock import AsyncMock, Mock

import pytest
from typing import cast, Any
from datetime import datetime
from bson import ObjectId
from result import Ok, Err
from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.exception import HubMemberNotFoundError
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


def _fields_are_correct(expected: HubMember, result: HubMember) -> bool:
    return (
        result.name == expected.name
        and str(result.id) == str(expected.id)
        and result.position == expected.position
        and result.department == expected.department
        and result.avatar_url == expected.avatar_url
    )


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> HubMembersRepository:
    return HubMembersRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_hub_member_success(
    ten_sec_window: tuple[datetime, datetime],
    hub_member_mock: HubMember,
    repo: HubMembersRepository,
) -> None:
    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(hub_member_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)
    assert _fields_are_correct(result.ok_value, hub_member_mock)
    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_hub_member_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, hub_member_mock: HubMember, repo: HubMembersRepository
) -> None:
    # Given
    # Simulate a general exception raised by insert_one
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("Test error"))

    # When
    result = await repo.create(hub_member_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_delete_hub_member_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    hub_member_dump_no_id_mock: dict[str, Any],
    obj_id_mock: str,
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        return_value=hub_member_dump_no_id_mock
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)
    assert result.ok_value.id == ObjectId(obj_id_mock)


@pytest.mark.asyncio
async def test_delete_hub_member_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: HubMembersRepository
) -> None:
    # Given
    # When the hub member with the specified object id is not found find_one_and_delete returns None
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_delete_hub_member_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: HubMembersRepository
) -> None:
    # Given
    # Simulate a general exception raised by find_one_and_delete
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
async def test_update_hub_member_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    hub_member_dump_no_id_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:
    # Given
    updated_doc = hub_member_dump_no_id_mock.copy()
    updated_doc["name"] = "Updated Name"
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=updated_doc)
    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(name="Updated Name"))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.id == ObjectId(obj_id_mock)
    assert result.ok_value.name == "Updated Name"


@pytest.mark.asyncio
async def test_update_hub_member_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: HubMembersRepository
) -> None:
    # Given
    # When a hub member with the specified id is not found find_one_and_update returns none
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(name="Updated Name"))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_update_hub_member_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        side_effect=Exception("Test error")
    )

    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(name="Updated Name"))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    # Check that the error message is the one in the Exception
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_fetch_by_id_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    hub_member_dump_no_id_mock: dict[str, Any],
    hub_member_mock: HubMember,
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=hub_member_dump_no_id_mock)

    # When
    result = await repo.fetch_by_id(str(hub_member_mock.id))

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)
    assert _fields_are_correct(hub_member_mock, result.ok_value)


@pytest.mark.asyncio
async def test_fetch_by_id_hub_member_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(side_effect=Exception("Test Error"))

    # When
    result = await repo.fetch_by_id(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: HubMembersRepository,
    hub_member_mock: HubMember,
) -> None:
    # Given
    mock_hub_members_data = [
        {
            "_id": hub_member_mock.id,
            "name": hub_member_mock.name,
            "position": hub_member_mock.position,
            "department": hub_member_mock.department,
            "avatar_url": hub_member_mock.avatar_url,
            "member_type": hub_member_mock.member_type,
            "social_links": {},
            "created_at": hub_member_mock.created_at,
            "updated_at": hub_member_mock.updated_at,
        }
        for _ in range(5)
    ]
    db_cursor_mock.to_list.return_value = mock_hub_members_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, member in enumerate(result.ok_value):
        assert member.name == mock_hub_members_data[i]["name"]
        assert member.position == mock_hub_members_data[i]["position"]
        assert member.department == mock_hub_members_data[i]["department"]
        assert member.avatar_url == mock_hub_members_data[i]["avatar_url"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: Mock,
    db_cursor_mock: MotorDbCursorMock,
    repo: HubMembersRepository,
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
    repo: HubMembersRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.side_effect = Exception("Test error")
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
