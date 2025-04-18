from unittest import mock
import pytest
from httpx import AsyncClient
from result import Err

PING_ENDPOINT_URL = "/api/v3/ping"


@pytest.mark.asyncio
async def test_ping_endpoint_service_unavailable(async_client: AsyncClient) -> None:
    with mock.patch("src.database.mongo.db_manager.MongoDatabaseManager.async_ping_db", return_value=Err("Test err")):
        # When
        resp = await async_client.get(PING_ENDPOINT_URL)

        # Then
        assert resp.status_code == 503
        assert resp.json() == {"error": "Database not available!"}


@pytest.mark.asyncio
async def test_ping_endpoint(async_client: AsyncClient) -> None:
    # When
    resp = await async_client.get(PING_ENDPOINT_URL)

    # Then
    assert resp.status_code == 200
    assert resp.json() == {"message": "pong"}
