import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_sponsors_list_returns_501(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v3/admin/sponsors")
    assert resp.status_code == 501
    assert resp.json()["detail"] == "Not implemented"
