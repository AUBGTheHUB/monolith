from typing import cast
from unittest.mock import ANY

import pytest
from result import Ok, Err

from src.database.model.admin.hub_admin_model import HubAdmin, AssignableRole
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import HubMemberNotFoundError
from src.service.user.user_service import UserService
from tests.unit_tests.conftest import HubMembersRepoMock, RefreshTokenRepoMock


@pytest.fixture
def user_service(
    hub_members_repo_mock: HubMembersRepoMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
) -> UserService:
    return UserService(
        hub_members_repo=cast(HubMembersRepository, hub_members_repo_mock),
        refresh_token_repo=cast(RefreshTokenRepository, refresh_token_repo_mock),
    )


async def test_change_role_success(
    user_service: UserService,
    hub_members_repo_mock: HubMembersRepoMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    hub_admin_mock: HubAdmin,
) -> None:
    """Tests successful role change and token invalidation."""
    # Arrange
    user_id = hub_admin_mock.id
    new_role = AssignableRole.BOARD

    hub_members_repo_mock.update.return_value = Ok(hub_admin_mock)
    refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.return_value = Ok(None)

    # Act
    result = await user_service.change_role(str(user_id), new_role)

    # Assert
    assert result.is_ok()
    assert result.unwrap() == hub_admin_mock

    # Verify repo calls
    hub_members_repo_mock.update.assert_called_once_with(user_id, ANY)
    refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.assert_called_once_with(user_id)


async def test_change_role_member_not_found(
    user_service: UserService, hub_members_repo_mock: HubMembersRepoMock, refresh_token_repo_mock: RefreshTokenRepoMock
) -> None:
    """Tests that service returns error immediately if user is not found."""
    # Arrange
    user_id = "missing_id"
    error = HubMemberNotFoundError(user_id)
    hub_members_repo_mock.update.return_value = Err(error)

    # Act
    result = await user_service.change_role(user_id, AssignableRole.DEV)

    # Assert
    assert result.is_err()
    assert result.err_value == error
    # Token invalidation should NOT be called if update fails
    refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.assert_not_called()


async def test_change_role_token_invalidation_fails_gracefully(
    user_service: UserService,
    hub_members_repo_mock: HubMembersRepoMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    hub_admin_mock: HubAdmin,
) -> None:
    """
    Tests that if token invalidation fails, the service still returns Ok.
    This matches the logic: if is_err(invalidation_result): LOG.error(...)
    """
    # Arrange
    user_id = hub_admin_mock.id
    hub_members_repo_mock.update.return_value = Ok(hub_admin_mock)
    # Simulate a database failure for tokens
    refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.return_value = Err(Exception("DB Error"))

    # Act
    result = await user_service.change_role(str(user_id), AssignableRole.BOARD)

    # Assert
    assert result.is_ok()
    assert result.unwrap() == hub_admin_mock
    refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.assert_called_once_with(user_id)


async def test_change_role_generic_exception(
    user_service: UserService, hub_members_repo_mock: HubMembersRepoMock
) -> None:
    """Tests handling of unexpected repository exceptions."""
    # Arrange
    user_id = "user_123"
    generic_error = Exception("Unexpected failure")
    hub_members_repo_mock.update.return_value = Err(generic_error)

    # Act
    result = await user_service.change_role(user_id, AssignableRole.DEV)

    # Assert
    assert result.is_err()
    assert result.err_value == generic_error
