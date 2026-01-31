from typing import cast
import pytest
from result import Err, Ok
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import (
    DuplicateHUBMemberNameError,
    HubMemberNotFoundError,
    PasswordsMismatchError,
    RefreshTokenNotFound,
)
from src.service.auth.auth_service import AuthService
from src.service.auth.auth_token_service import AuthTokenService
from src.service.auth.password_hash_service import PasswordHashService
from src.database.model.admin.hub_admin_model import HubAdmin
from src.database.model.admin.refresh_token import RefreshToken
from src.service.jwt_utils.schemas import JwtRefreshToken
from tests.unit_tests.conftest import (
    AuthTokensServiceMock,
    HubMembersRepoMock,
    MongoTransactionManagerMock,
    PasswordHashServiceMock,
    RefreshTokenRepoMock,
)
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData, RegisterHubAdminData

from tests.integration_tests.conftest import TEST_HUB_ADMIN_PASSWORD_HASH


@pytest.fixture
def auth_service(
    hub_members_repo_mock: HubMembersRepoMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    password_hash_service_mock: PasswordHashServiceMock,
    tx_manager_mock: MongoTransactionManagerMock,
) -> AuthService:
    return AuthService(
        cast(HubMembersRepository, hub_members_repo_mock),
        cast(RefreshTokenRepository, refresh_token_repo_mock),
        cast(PasswordHashService, password_hash_service_mock),
        cast(AuthTokenService, auth_tokens_service_mock),
        cast(MongoTransactionManager, tx_manager_mock),
    )


@pytest.mark.asyncio
async def test_register_hub_admin_success(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    hub_admin_mock: HubAdmin,
    register_hub_admin_data_mock: RegisterHubAdminData,
) -> None:

    # Given
    password_hash_service_mock.hash_password.return_value = TEST_HUB_ADMIN_PASSWORD_HASH.encode("utf-8")
    hub_members_repo_mock.check_if_admin_exists_by_name.return_value = Ok(False)
    hub_members_repo_mock.create.return_value = Ok(hub_admin_mock)

    # When
    result = await auth_service.register_admin(register_hub_admin_data_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, HubAdmin)


@pytest.mark.asyncio
async def test_register_hub_admin_fails_when_name_is_duplicate(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    register_hub_admin_data_mock: RegisterHubAdminData,
) -> None:

    # Given
    password_hash_service_mock.hash_password.return_value = TEST_HUB_ADMIN_PASSWORD_HASH.encode("utf-8")
    hub_members_repo_mock.check_if_admin_exists_by_name.return_value = Ok(True)
    hub_members_repo_mock.create.return_value = Err(DuplicateHUBMemberNameError())

    # When
    result = await auth_service.register_admin(register_hub_admin_data_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateHUBMemberNameError)


@pytest.mark.asyncio
async def test_register_hub_admin_fails_general_error(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    register_hub_admin_data_mock: RegisterHubAdminData,
) -> None:

    # Given
    password_hash_service_mock.hash_password.return_value = TEST_HUB_ADMIN_PASSWORD_HASH.encode("utf-8")
    hub_members_repo_mock.check_if_admin_exists_by_name.return_value = Ok(False)
    hub_members_repo_mock.create.return_value = Err(Exception())

    # When
    result = await auth_service.register_admin(register_hub_admin_data_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_login_hub_admin_success(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    login_hub_admin_data_mock: LoginHubAdminData,
    hub_admin_mock: HubAdmin,
    refresh_token_mock: RefreshToken,
) -> None:

    # Given
    hub_members_repo_mock.fetch_admin_by_name.return_value = Ok(hub_admin_mock)
    password_hash_service_mock.check_password.return_value = True
    auth_tokens_service_mock.generate_auth_token.return_value = "token_1"
    refresh_token_repo_mock.create.return_value = Ok(refresh_token_mock)
    auth_tokens_service_mock.generate_refresh_token.return_value = "token_2"

    # When
    result = await auth_service.login_admin(login_hub_admin_data_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert result.ok_value[0] == "token_1"
    assert result.ok_value[1] == "token_2"


@pytest.mark.asyncio
async def test_login_hub_admin_not_found(
    auth_service: AuthService, hub_members_repo_mock: HubMembersRepoMock, login_hub_admin_data_mock: LoginHubAdminData
) -> None:

    # Given
    hub_members_repo_mock.fetch_admin_by_name.return_value = Err(HubMemberNotFoundError())

    # When
    result = await auth_service.login_admin(login_hub_admin_data_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_login_hub_admin_passwords_mismatch(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    login_hub_admin_data_mock: LoginHubAdminData,
    hub_admin_mock: HubAdmin,
) -> None:

    # Given
    hub_members_repo_mock.fetch_admin_by_name.return_value = Ok(hub_admin_mock)
    password_hash_service_mock.check_password.return_value = False

    # When
    result = await auth_service.login_admin(login_hub_admin_data_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, PasswordsMismatchError)


@pytest.mark.asyncio
async def test_login_hub_admin_could_not_create_refresh_token(
    auth_service: AuthService,
    password_hash_service_mock: PasswordHashServiceMock,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    login_hub_admin_data_mock: LoginHubAdminData,
    hub_admin_mock: HubAdmin,
) -> None:

    # Given
    hub_members_repo_mock.fetch_admin_by_name.return_value = Ok(hub_admin_mock)
    password_hash_service_mock.check_password.return_value = True
    auth_tokens_service_mock.generate_auth_token.return_value = "token_1"
    refresh_token_repo_mock.create.return_value = Err(Exception())

    # When
    result = await auth_service.login_admin(login_hub_admin_data_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_refresh_token_success(
    auth_service: AuthService,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
    hub_admin_mock: HubAdmin,
    jwt_refresh_token_mock: JwtRefreshToken,
    refresh_token_mock: RefreshToken,
) -> None:

    # Given
    auth_tokens_service_mock.decode_refresh_token.return_value = Ok(jwt_refresh_token_mock)
    refresh_token_repo_mock.fetch_by_id.return_value = Ok(refresh_token_mock)
    hub_members_repo_mock.fetch_by_id.return_value = Ok(hub_admin_mock)

    auth_tokens_service_mock.generate_auth_token.return_value = "token_1"
    tx_manager_mock.with_transaction.return_value = Ok(refresh_token_mock)
    auth_tokens_service_mock.generate_refresh_token.return_value = "token_2"

    # When
    result = await auth_service.refresh_token("refresh")

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert result.ok_value[0] == "token_1"
    assert result.ok_value[1] == "token_2"


@pytest.mark.asyncio
async def test_refresh_token_decode_error(
    auth_service: AuthService,
    auth_tokens_service_mock: AuthTokensServiceMock,
) -> None:

    # Given
    auth_tokens_service_mock.decode_refresh_token.return_value = Err(Exception())

    # When
    result = await auth_service.refresh_token("refresh")

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_refresh_token_not_found(
    auth_service: AuthService,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    jwt_refresh_token_mock: JwtRefreshToken,
) -> None:

    # Given
    auth_tokens_service_mock.decode_refresh_token.return_value = Ok(jwt_refresh_token_mock)
    refresh_token_repo_mock.fetch_by_id.return_value = Err(RefreshTokenNotFound())

    # When
    result = await auth_service.refresh_token("refresh")

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, RefreshTokenNotFound)


@pytest.mark.asyncio
async def test_refresh_token_hub_admin_not_found(
    auth_service: AuthService,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    jwt_refresh_token_mock: JwtRefreshToken,
    refresh_token_mock: RefreshToken,
) -> None:

    # Given
    auth_tokens_service_mock.decode_refresh_token.return_value = Ok(jwt_refresh_token_mock)
    refresh_token_repo_mock.fetch_by_id.return_value = Ok(refresh_token_mock)
    hub_members_repo_mock.fetch_by_id.return_value = Err(HubMemberNotFoundError())

    # When
    result = await auth_service.refresh_token("refresh")

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HubMemberNotFoundError)


@pytest.mark.asyncio
async def test_refresh_token_transaction_failed(
    auth_service: AuthService,
    refresh_token_repo_mock: RefreshTokenRepoMock,
    auth_tokens_service_mock: AuthTokensServiceMock,
    hub_members_repo_mock: HubMembersRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
    hub_admin_mock: HubAdmin,
    jwt_refresh_token_mock: JwtRefreshToken,
    refresh_token_mock: RefreshToken,
) -> None:

    # Given
    auth_tokens_service_mock.decode_refresh_token.return_value = Ok(jwt_refresh_token_mock)
    refresh_token_repo_mock.fetch_by_id.return_value = Ok(refresh_token_mock)
    hub_members_repo_mock.fetch_by_id.return_value = Ok(hub_admin_mock)

    auth_tokens_service_mock.generate_auth_token.return_value = "token_1"
    tx_manager_mock.with_transaction.return_value = Err(Exception())

    # When
    result = await auth_service.refresh_token("refresh")

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
