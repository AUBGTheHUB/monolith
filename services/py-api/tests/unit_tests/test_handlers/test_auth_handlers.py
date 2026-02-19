from typing import cast
from fastapi import HTTPException
from starlette.responses import Response as StarletteResponse
import pytest
from result import Err, Ok
from src.exception import (
    DuplicateHubMemberUsernameError,
    HubMemberNotFoundError,
    JwtExpiredSignatureError,
    PasswordsMismatchError,
    RefreshTokenNotFound,
)
from starlette import status

from src.database.model.admin.hub_admin_model import HubAdmin
from src.server.handlers.auth.auth_handlers import AuthHandlers
from src.server.schemas.request_schemas.auth.schemas import RegisterHubAdminData, LoginHubAdminData
from src.server.schemas.response_schemas.auth.schemas import AuthTokensSuccessfullyIssued, AccessTokenSuccessfullyIssued
from src.server.schemas.response_schemas.schemas import ErrResponse, Response
from src.service.auth.auth_service import AuthService
from tests.unit_tests.conftest import AuthServiceMock


@pytest.fixture
def auth_handlers(auth_service_mock: AuthServiceMock) -> AuthHandlers:
    return AuthHandlers(
        cast(AuthService, auth_service_mock),
    )


@pytest.mark.asyncio
async def test_register_hub_admin_success(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
    hub_admin_mock: HubAdmin,
    register_hub_admin_data_mock: RegisterHubAdminData,
) -> None:
    # Given
    auth_service_mock.register_admin.return_value = Ok(hub_admin_mock)

    # When
    resp = await auth_handlers.register(credentials=register_hub_admin_data_mock)

    # Then
    assert isinstance(resp, StarletteResponse)
    assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_register_hub_admin_conflict(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
    register_hub_admin_data_mock: RegisterHubAdminData,
) -> None:
    with pytest.raises(HTTPException) as exception:

        # Given
        auth_service_mock.register_admin.return_value = Err(DuplicateHubMemberUsernameError())

        # When
        await auth_handlers.register(credentials=register_hub_admin_data_mock)

        # Then
        assert exception.value.detail == "HUB member with this name already exists"
        assert exception.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_login_hub_admin_success(
    auth_handlers: AuthHandlers, auth_service_mock: AuthServiceMock, login_hub_admin_data_mock: LoginHubAdminData
) -> None:
    # Given
    auth_service_mock.login_admin.return_value = Ok(("token_1", "token_2", "token_3"))

    # When
    resp = await auth_handlers.login(credentials=login_hub_admin_data_mock)
    cookies = resp.headers.getlist("Set-Cookie")

    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, AuthTokensSuccessfullyIssued)
    assert resp.response_model.access_token == "token_1"
    assert any("refresh_token=token_3" in c for c in cookies)
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_login_hub_admin_wrong_password(
    auth_handlers: AuthHandlers, auth_service_mock: AuthServiceMock, login_hub_admin_data_mock: LoginHubAdminData
) -> None:
    # Given
    auth_service_mock.login_admin.return_value = Err(PasswordsMismatchError())

    # When
    resp = await auth_handlers.login(credentials=login_hub_admin_data_mock)

    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.response_model.error == "The name and password do not match!"


@pytest.mark.asyncio
async def test_login_hub_admin_not_found(
    auth_handlers: AuthHandlers, auth_service_mock: AuthServiceMock, login_hub_admin_data_mock: LoginHubAdminData
) -> None:
    # Given
    auth_service_mock.login_admin.return_value = Err(HubMemberNotFoundError())

    # When
    resp = await auth_handlers.login(credentials=login_hub_admin_data_mock)

    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.response_model.error == "The hub member was not found."


@pytest.mark.asyncio
async def test_refresh_token_success(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
) -> None:
    # Given
    auth_service_mock.refresh_token.return_value = Ok(("token_1", "token_2"))

    # When
    resp = await auth_handlers.refresh_token_pair(refresh_token="token_2")
    cookies = resp.headers.getlist("Set-Cookie")

    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, AccessTokenSuccessfullyIssued)
    assert resp.response_model.access_token == "token_1"
    assert resp.status_code == status.HTTP_200_OK
    assert any("refresh_token=token_2" in c for c in cookies)


@pytest.mark.asyncio
async def test_refresh_token_not_found(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
) -> None:
    # Given
    auth_service_mock.refresh_token.return_value = Err(RefreshTokenNotFound())

    # When
    resp = await auth_handlers.refresh_token_pair(refresh_token="token_2")
    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The refresh token was not found."
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_hub_admin_not_found_for_refresh_token(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
) -> None:
    # Given
    auth_service_mock.refresh_token.return_value = Err(HubMemberNotFoundError())

    # When
    resp = await auth_handlers.refresh_token_pair(refresh_token="token_2")
    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The hub member was not found."
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_expired_refresh_token(
    auth_handlers: AuthHandlers,
    auth_service_mock: AuthServiceMock,
) -> None:
    # Given
    auth_service_mock.refresh_token.return_value = Err(JwtExpiredSignatureError())

    # When
    resp = await auth_handlers.refresh_token_pair(refresh_token="token_2")
    # Then
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The JWT token has expired."
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
