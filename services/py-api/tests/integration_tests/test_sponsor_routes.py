from os import environ
from unittest.mock import patch
import pytest
from httpx import AsyncClient

from tests.integration_tests.conftest import async_client
from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams

SPONSORS_ENDPOINT_URL = "/api/v3/admin/sponsors"

TEST_SPONSOR_NAME = "Coca-Cola"
TEST_SPONSOR_TIER = "GOLD"
TEST_SPONSOR_LOGO_URL = "https://eu.aws.com/coca-cola.jpg"
TEST_SPONSOR_WEBSITE_URL = "https://coca-cola.com"

@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_create_sponsor_success(async_client: AsyncClient) -> None:
    # Given

    sponsor_body = Sponsor(TEST_SPONSOR_NAME, TEST_SPONSOR_TIER, TEST_SPONSOR_LOGO_URL, TEST_SPONSOR_WEBSITE_URL)

    auth_header = {"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}

    # When
    response = await async_client.post(
        SPONSORS_ENDPOINT_URL,
        json=sponsor_body,
        headers=auth_header
    )

    # Then
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["name"] == TEST_SPONSOR_NAME
    assert response_json["tier"] == TEST_SPONSOR_TIER
    assert response_json["logo_url"] == TEST_SPONSOR_LOGO_URL
    assert response_json["website_url"] == TEST_SPONSOR_WEBSITE_URL
    assert "id" in response_json

    # Cleanup
    sponsor_id = response_json["id"]
    await async_client.delete(f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}", headers=auth_header)

# @patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
# @pytest.mark.asyncio
# async def test_create_sponsor_missing_field(async_client: AsyncClient) -> None:
#     # Given
#     sponsor_body = Sponsor(
#         name: TEST_SPONSOR_NAME,
#         tier: TEST_SPONSOR_TIER,
#         logo_url: TEST_SPONSOR_LOGO_URL
#     )

#     auth_header = {"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}

#     # When
#     response = await async_client.post(
#         SPONSORS_ENDPOINT_URL,
#         json=sponsor_body,
#         headers=auth_header
#     )

#     # Then
#     assert response.status_code == 400
#     response_json = response.json()
#     assert resp_json["detail"][0]["msg"] == "Field required"


# @patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
# @pytest.mark.asyncio
# async def test_create_sponsor_missing_field(async_client: AsyncClient) -> None:
    