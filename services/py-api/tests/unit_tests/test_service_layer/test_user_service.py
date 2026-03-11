from typing import cast, Any
from unittest.mock import ANY

import pytest
from result import Ok, Err

from src.database.model.admin.hub_admin_model import HubAdmin, AssignableRole
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import HubMemberNotFoundError
from src.service.user.user_service import UserService
from tests.unit_tests.conftest import HubMembersRepoMock, RefreshTokenRepoMock, MongoTransactionManagerMock


@pytest.fixture
def user_service(
    hub_members_repo_mock: HubMembersRepoMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
) -> UserService:
    # Define an async wrapper to simulate the transaction manager's behavior
    async def async_transaction_side_effect(callback: Any, **kwargs: Any) -> Any:
        return await callback(**kwargs)

    # Assign the async wrapper to the side_effect
    tx_manager_mock.with_transaction.side_effect = async_transaction_side_effect

    return UserService(
        hub_members_repo=cast(HubMembersRepository, hub_members_repo_mock),
        refresh_token_repo=cast(RefreshTokenRepository, refresh_token_repo_mock),
        tx_manager=cast(MongoTransactionManager, tx_manager_mock),
    )


@pytest.mark.asyncio
class TestUserService:

    async def test_change_role_success(
        self,
        user_service: UserService,
        hub_members_repo_mock: HubMembersRepoMock,
        refresh_token_repo_mock: RefreshTokenRepoMock,
        tx_manager_mock: MongoTransactionManagerMock,
        hub_admin_mock: HubAdmin,
    ) -> None:
        """Tests successful role change inside a transaction."""
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

        # Verify transaction manager was used
        tx_manager_mock.with_transaction.assert_called_once()

        # Verify repo calls
        hub_members_repo_mock.update.assert_called_once_with(user_id, ANY, session=None)
        refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.assert_called_once_with(user_id, session=None)

    async def test_change_role_member_not_found(
        self,
        user_service: UserService,
        hub_members_repo_mock: HubMembersRepoMock,
        refresh_token_repo_mock: RefreshTokenRepoMock,
    ) -> None:
        """Tests that if user update fails, the transaction returns the error and skips token invalidation."""
        # Arrange
        user_id = "missing_id"
        error = HubMemberNotFoundError(user_id)
        hub_members_repo_mock.update.return_value = Err(error)

        # Act
        result = await user_service.change_role(user_id, AssignableRole.DEV)

        # Assert
        assert result.is_err()
        assert result.err_value == error
        # Ensure we didn't proceed to invalidate tokens
        refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.assert_not_called()

    async def test_change_role_token_invalidation_failure(
        self,
        user_service: UserService,
        hub_members_repo_mock: HubMembersRepoMock,
        refresh_token_repo_mock: RefreshTokenRepoMock,
        hub_admin_mock: HubAdmin,
    ) -> None:
        """
        Per new logic: If token invalidation fails, the service returns the error
        (likely triggering a transaction rollback).
        """
        # Arrange
        user_id = hub_admin_mock.id
        hub_members_repo_mock.update.return_value = Ok(hub_admin_mock)

        token_error = Exception("Redis/DB Error")
        refresh_token_repo_mock.invalidate_all_tokens_by_hub_member_id.return_value = Err(token_error)

        # Act
        result = await user_service.change_role(str(user_id), AssignableRole.BOARD)

        # Assert
        assert result.is_err()
        assert result.err_value == token_error
        # Verify the update was still called before the failure
        hub_members_repo_mock.update.assert_called_once()

    async def test_change_role_transaction_exception(
        self, user_service: UserService, tx_manager_mock: MongoTransactionManagerMock
    ) -> None:
        """Tests handling when the transaction manager itself encounters an exception."""
        # Arrange
        tx_manager_mock.with_transaction.side_effect = Exception("Atomic failure")

        # Act & Assert
        with pytest.raises(Exception, match="Atomic failure"):
            await user_service.change_role("123", AssignableRole.DEV)

    async def test_fetch_all_admins_success(
        self, user_service: UserService, hub_members_repo_mock: HubMembersRepoMock, hub_admin_dict_mock: dict[str, Any]
    ) -> None:

        # Given
        hub_members_repo_mock.fetch_all_filtered.return_value = Ok(hub_admin_dict_mock)

        # When
        result = await user_service.get_all_admins()

        # Then
        assert isinstance(result, Ok)
        assert result.unwrap() == hub_admin_dict_mock
        hub_members_repo_mock.fetch_all_filtered.assert_awaited_once()

    async def test_fetch_all_admins_success_with_no_admins(
        self, user_service: UserService, hub_members_repo_mock: HubMembersRepoMock
    ) -> None:

        # Given
        hub_members_repo_mock.fetch_all_filtered.return_value = Ok([])

        # When
        result = await user_service.get_all_admins()

        # Then
        assert isinstance(result, Ok)
        assert result.unwrap() == []
        hub_members_repo_mock.fetch_all_filtered.assert_awaited_once()

    async def test_fetch_all_admins_general_exception(
        self, user_service: UserService, hub_members_repo_mock: HubMembersRepoMock
    ) -> None:

        # Given
        hub_members_repo_mock.fetch_all_filtered.return_value = Err(Exception("General Exceptiom"))

        # When
        result = await user_service.get_all_admins()

        # Then
        assert isinstance(result, Err)
        hub_members_repo_mock.fetch_all_filtered.assert_awaited_once()
