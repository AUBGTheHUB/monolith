from io import BytesIO
from typing import Generator, Any

import pytest
import uuid
from httpx import AsyncClient
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData
from tests.integration_tests.conftest import (
    TEST_HUB_ADMIN_PASSWORD_HASH,
    RegisterHubAdminBodyCallable,
)

AUTH_ENDPOINT_URL = "/api/v3/auth"


@pytest.mark.asyncio
async def test_register_admin_success(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
    image_mock: BytesIO,  # Use existing image fixture
) -> None:
    # When
    unique_name = str(uuid.uuid4())
    data = generate_register_hub_admin_request_body(username=unique_name, name=unique_name)

    files = {"avatar": image_mock}

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=data, files=files)

    # Then
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_register_admin_fails_when_there_is_a_duplicate_name(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
    image_mock: BytesIO,
) -> None:
    # When
    data = generate_register_hub_admin_request_body()
    files = {"avatar": image_mock}
    # First request
    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=data, files=files)
    assert resp.status_code == 204

    # Reset stream for second request
    image_mock.seek(0)

    # Second request
    resp2 = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=data, files=files)

    # Then
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_login_admin_success(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
    image_mock: BytesIO,
) -> None:
    # 1. Register the user using multipart/form-data
    register_data = generate_register_hub_admin_request_body()
    files = {"avatar": image_mock}
    register_resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=register_data, files=files)
    assert register_resp.status_code == 204
    # When
    login_hub_admin_data = LoginHubAdminData(username=register_data["username"], password=TEST_HUB_ADMIN_PASSWORD_HASH)

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_login_admin_fails_when_passwords_dont_match(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
    image_mock: BytesIO,
) -> None:
    register_data = generate_register_hub_admin_request_body()
    files = {"avatar": image_mock}
    register_resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=register_data, files=files)
    assert register_resp.status_code == 204
    # When
    login_hub_admin_data = LoginHubAdminData(username=register_data["username"], password="Another hash")

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_admin_fails_when_hub_admin_is_not_found(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # When
    login_hub_admin_data = LoginHubAdminData(username="Wrong username", password=TEST_HUB_ADMIN_PASSWORD_HASH)

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_refresh_token_success(
    aws_mock: Generator[None, Any, None],
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
    image_mock: BytesIO,
) -> None:
    register_data = generate_register_hub_admin_request_body()
    files = {"avatar": image_mock}
    register_resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", data=register_data, files=files)
    assert register_resp.status_code == 204
    # When
    login_hub_admin_data = LoginHubAdminData(username=register_data["username"], password=TEST_HUB_ADMIN_PASSWORD_HASH)
    tokens_result = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())
    tokens_result.cookies.get("refresh_token")

    resp = await async_client.post(
        f"{AUTH_ENDPOINT_URL}/refresh", cookies={"refresh_token": tokens_result.cookies.get("refresh_token")}
    )

    # Then
    assert resp.status_code == 200
    assert resp.cookies.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_refresh_token_fails_for_invalid_refresh_token(
    async_client: AsyncClient,
) -> None:
    resp = await async_client.post(
        f"{AUTH_ENDPOINT_URL}/refresh", cookies={"refresh_token": "Some invalid refresh token"}
    )

    # Then
    assert resp.status_code == 400
