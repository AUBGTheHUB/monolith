import pytest
import uuid
from httpx import AsyncClient
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData
from tests.integration_tests.conftest import (
    TEST_HUB_ADMIN_PASSWORD_HASH,
    TEST_HUB_MEMBER_NAME,
    RegisterHubAdminBodyCallable,
)

AUTH_ENDPOINT_URL = "/api/v3/auth"


@pytest.mark.asyncio
async def test_register_admin_success(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # When
    unique_name = str(uuid.uuid1())
    register_hub_admin_body = generate_register_hub_admin_request_body(name=unique_name)

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # Then
    assert resp.status_code == 201
    assert resp.json()["hub_admin"]["name"] == unique_name


@pytest.mark.asyncio
async def test_register_admin_fails_when_there_is_a_duplicate_name(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # When
    register_hub_admin_body = generate_register_hub_admin_request_body()

    # Fire the request twice so it fails the second time
    await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    resp2 = await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # Then
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_login_admin_success(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # Register the user
    register_hub_admin_body = generate_register_hub_admin_request_body()
    await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # When
    login_hub_admin_data = LoginHubAdminData(name=TEST_HUB_MEMBER_NAME, password=TEST_HUB_ADMIN_PASSWORD_HASH)

    # Fire the request twice so it fails the second time
    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_login_admin_fails_when_passwords_dont_match(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # Register the user
    register_hub_admin_body = generate_register_hub_admin_request_body()
    await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # When
    login_hub_admin_data = LoginHubAdminData(name=TEST_HUB_MEMBER_NAME, password="Another hash")

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_admin_fails_when_hub_admin_is_not_found(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # Register the user
    register_hub_admin_body = generate_register_hub_admin_request_body()
    await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # When
    login_hub_admin_data = LoginHubAdminData(name="Wrong username", password=TEST_HUB_ADMIN_PASSWORD_HASH)

    resp = await async_client.post(f"{AUTH_ENDPOINT_URL}/login", json=login_hub_admin_data.model_dump())

    # Then
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_refresh_token_success(
    async_client: AsyncClient,
    generate_register_hub_admin_request_body: RegisterHubAdminBodyCallable,
) -> None:
    # Register the user
    register_hub_admin_body = generate_register_hub_admin_request_body()
    await async_client.post(f"{AUTH_ENDPOINT_URL}/register", json=register_hub_admin_body.model_dump())

    # When
    login_hub_admin_data = LoginHubAdminData(name=TEST_HUB_MEMBER_NAME, password=TEST_HUB_ADMIN_PASSWORD_HASH)
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
