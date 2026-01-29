import pytest
from datetime import datetime
from typing import Any, cast
from unittest.mock import AsyncMock

from pymongo.errors import DuplicateKeyError
from result import Ok, Err

from src.database.model.admin.hub_admin_model import HubAdmin
from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository

from src.exception import DuplicateHUBMemberNameError, HubMemberNotFoundError
from structlog.stdlib import get_logger
from tests.integration_tests.conftest import (
    TEST_HUB_MEMBER_NAME,
    TEST_HUB_ADMIN_MEMBER_TYPE,
    TEST_HUB_MEMBER_MEMBER_TYPE,
    TEST_HUB_ADMIN_PASSWORD_HASH,
    TEST_HUB_ADMIN_ROLE,
    TEST_HUB_MEMBER_SOCIAL_LINKS,
    TEST_HUB_MEMBER_POSITON,
    TEST_HUB_MEMBER_AVATAR_URL,
    TEST_HUB_MEMBER_DEPARTMENT,
)
from tests.unit_tests.conftest import MongoDbManagerMock, MotorDbCursorMock


LOG = get_logger()


@pytest.fixture
def repo(mongo_db_manager_mock: MongoDbManagerMock) -> HubMembersRepository:
    return HubMembersRepository(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_create_hub_admin_success(
    ten_sec_window: tuple[datetime, datetime], hub_admin_mock: HubAdmin, repo: HubMembersRepository
) -> None:

    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(hub_member=hub_admin_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubAdmin)
    assert result.ok_value.name == hub_admin_mock.name

    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_hub_member_success(
    ten_sec_window: tuple[datetime, datetime], hub_member_mock: HubMember, repo: HubMembersRepository
) -> None:

    # Given
    start_time, end_time = ten_sec_window

    # When
    result = await repo.create(hub_member=hub_member_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)
    assert result.ok_value.name == hub_member_mock.name

    # Check that created_at and updated_at fall within the 10-second window
    assert start_time <= result.ok_value.created_at <= end_time, "created_at is not within the 10-second window"
    assert start_time <= result.ok_value.updated_at <= end_time, "updated_at is not within the 10-second window"


@pytest.mark.asyncio
async def test_create_duplicate_hub_member_error(
    mongo_db_manager_mock: MongoDbManagerMock, hub_member_mock: HubMember, repo: HubMembersRepository
) -> None:
    # Given
    # Simulate a DuplicateKeyError raised when trying to insert a hub member with a duplicate name
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(
        side_effect=DuplicateKeyError("Duplicate hub member name")
    )

    # When
    result = await repo.create(hub_member_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateHUBMemberNameError)


@pytest.mark.asyncio
async def test_create_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock, hub_member_mock: HubMember, repo: HubMembersRepository
) -> None:
    # Given
    # Simulate a General Exception
    mongo_db_manager_mock.get_collection.return_value.insert_one = AsyncMock(side_effect=Exception("General Error"))

    # When
    result = await repo.create(hub_member_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_fetch_by_id_for_hub_member_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    hub_member_dict_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=hub_member_dict_mock)
    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)
    assert isinstance(result.ok_value, HubAdmin) == False
    assert result.ok_value.id == obj_id_mock
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.member_type == TEST_HUB_MEMBER_MEMBER_TYPE
    assert result.ok_value.social_links == TEST_HUB_MEMBER_SOCIAL_LINKS
    assert result.ok_value.position == TEST_HUB_MEMBER_POSITON
    assert result.ok_value.department == TEST_HUB_MEMBER_DEPARTMENT
    assert result.ok_value.avatar_url == TEST_HUB_MEMBER_AVATAR_URL


@pytest.mark.asyncio
async def test_fetch_by_id_for_hub_admin_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    hub_admin_dict_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=hub_admin_dict_mock)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubAdmin)
    assert result.ok_value.id == obj_id_mock
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.member_type == TEST_HUB_ADMIN_MEMBER_TYPE
    assert result.ok_value.social_links == TEST_HUB_MEMBER_SOCIAL_LINKS
    assert result.ok_value.position == TEST_HUB_MEMBER_POSITON
    assert result.ok_value.department == TEST_HUB_MEMBER_DEPARTMENT
    assert result.ok_value.avatar_url == TEST_HUB_MEMBER_AVATAR_URL
    assert result.ok_value.password_hash == TEST_HUB_ADMIN_PASSWORD_HASH
    assert result.ok_value.site_role == TEST_HUB_ADMIN_ROLE


@pytest.mark.asyncio
async def test_fetch_by_id_not_found(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_by_id(obj_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_fetch_by_id_general_error(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: HubMembersRepository,
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
async def test_delete_hub_member_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    hub_member_dict_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:

    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=hub_member_dict_mock)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubMember)

    assert result.ok_value.id == obj_id_mock
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.member_type == TEST_HUB_MEMBER_MEMBER_TYPE
    assert result.ok_value.department == TEST_HUB_MEMBER_DEPARTMENT


@pytest.mark.asyncio
async def test_delete_hub_admin_successful(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    hub_admin_dict_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=hub_admin_dict_mock)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubAdmin)

    assert result.ok_value.id == obj_id_mock
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.member_type == TEST_HUB_ADMIN_MEMBER_TYPE
    assert result.ok_value.department == TEST_HUB_MEMBER_DEPARTMENT


@pytest.mark.asyncio
async def test_delete_hub_member_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(return_value=None)

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_delete_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_delete = AsyncMock(
        side_effect=Exception("General Error")
    )

    # When
    result = await repo.delete(obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_update_hub_member_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    obj_id_mock: str,
    repo: HubMembersRepository,
    update_hub_member_dict_mock: dict[str, Any],
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        return_value=update_hub_member_dict_mock
    )

    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(department="Marketing"))

    # Then
    assert isinstance(result, Ok)
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.member_type == TEST_HUB_MEMBER_MEMBER_TYPE
    assert result.ok_value.department == "Marketing"


@pytest.mark.asyncio
async def test_update_hub_member_not_found(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: HubMembersRepository
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(return_value=None)

    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(department="Marketing"))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_update_hub_member_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, obj_id_mock: str, repo: HubMembersRepository
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one_and_update = AsyncMock(
        side_effect=Exception("General Error")
    )

    # When
    result = await repo.update(obj_id_mock, UpdateHubMemberParams(department="Marketing"))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_fetch_all_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: HubMembersRepository,
    hub_member_dict_mock: dict[str, Any],
) -> None:
    # Given
    # Prepare mock MongoDB documents
    mock_hub_members_data = [hub_member_dict_mock for _ in range(5)]
    db_cursor_mock.to_list.return_value = mock_hub_members_data
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    # Run the method
    result = await repo.fetch_all()

    # Then
    # Assertions
    assert isinstance(result, Ok)
    assert len(result.ok_value) == 5

    for i, hub_member in enumerate(result.ok_value):
        assert hub_member.name == mock_hub_members_data[i]["name"]
        assert hub_member.member_type == mock_hub_members_data[i]["member_type"]


@pytest.mark.asyncio
async def test_fetch_all_empty(
    mongo_db_manager_mock: MongoDbManagerMock,
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
async def test_fetch_all_general_exception(
    mongo_db_manager_mock: MongoDbManagerMock,
    db_cursor_mock: MotorDbCursorMock,
    repo: HubMembersRepository,
) -> None:
    # Given
    db_cursor_mock.to_list.side_effect = Exception("General Error")
    mongo_db_manager_mock.get_collection.return_value.find.return_value = db_cursor_mock

    # When
    result = await repo.fetch_all()

    # Then
    assert isinstance(result, Err)
    assert str(result.err_value) == "General Error"


@pytest.mark.asyncio
async def test_fetch_admin_by_name_success(
    mongo_db_manager_mock: MongoDbManagerMock,
    hub_admin_dict_mock: dict[str, Any],
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=hub_admin_dict_mock)

    # When
    result = await repo.fetch_admin_by_name(TEST_HUB_MEMBER_NAME)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubAdmin)
    assert result.ok_value.name == TEST_HUB_MEMBER_NAME
    assert result.ok_value.site_role == TEST_HUB_ADMIN_ROLE


@pytest.mark.asyncio
async def test_fetch_admin_by_name_not_found(
    mongo_db_manager_mock: MongoDbManagerMock,
    repo: HubMembersRepository,
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(return_value=None)

    # When
    result = await repo.fetch_admin_by_name(TEST_HUB_MEMBER_NAME)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def check_if_admin_exists_by_name_success(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(True)

    # When
    result = await repo.check_if_admin_exists_by_name(TEST_HUB_MEMBER_NAME)

    # Then
    assert isinstance(result, Ok)
    result.ok_value == True


@pytest.mark.asyncio
async def check_if_admin_exists_by_name_general_error(
    mongo_db_manager_mock: MongoDbManagerMock, repo: HubMembersRepository, obj_id_mock: str
) -> None:
    # Given
    mongo_db_manager_mock.get_collection.return_value.find_one = AsyncMock(side_effect=Exception("General Error"))

    # When
    result = await repo.check_if_admin_exists_by_name(TEST_HUB_MEMBER_NAME)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "General Error"
