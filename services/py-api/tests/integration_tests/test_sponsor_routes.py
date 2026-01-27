from os import environ
from typing import Any
from unittest.mock import patch
import pytest
from httpx import AsyncClient

SPONSORS_ENDPOINT_URL = "/api/v3/admin/sponsors"

TEST_SPONSOR_NAME = "Coca-Cola"
TEST_SPONSOR_TIER = "GOLD"
TEST_SPONSOR_LOGO_URL = "https://eu.aws.com/coca-cola.jpg"
TEST_SPONSOR_WEBSITE_URL = "https://coca-cola.com/"

valid_sponsor_body: dict[str, Any] = {
    "name": TEST_SPONSOR_NAME,
    "tier": TEST_SPONSOR_TIER,
    "logo_url": TEST_SPONSOR_LOGO_URL,
    "website_url": TEST_SPONSOR_WEBSITE_URL,
}


async def _delete_sponsor(async_client: AsyncClient, sponsor_id: str) -> None:
    await async_client.delete(
        url=f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_sponsor_success(async_client: AsyncClient) -> None:

    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "sponsor" in response_body
    assert response_body["sponsor"]["name"] == TEST_SPONSOR_NAME
    assert response_body["sponsor"]["tier"] == TEST_SPONSOR_TIER
    assert response_body["sponsor"]["logo_url"] == TEST_SPONSOR_LOGO_URL
    assert response_body["sponsor"]["website_url"] == TEST_SPONSOR_WEBSITE_URL
    assert "id" in response_body["sponsor"]

    # Cleanup
    sponsor_id = response_body["sponsor"]["id"]
    await _delete_sponsor(async_client, sponsor_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_sponsor_missing_parameter(async_client: AsyncClient) -> None:

    # Arrange
    invalid_sponsor_body: dict[str, Any] = {
        "name": TEST_SPONSOR_NAME,
        "tier": TEST_SPONSOR_TIER,
        "website_url": TEST_SPONSOR_WEBSITE_URL,
    }

    # Act
    response = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=invalid_sponsor_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()

    assert response_body["detail"][0]["type"] == "missing"
    assert "logo_url" in response_body["detail"][0]["loc"]


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_sponsor_unauthorized(async_client: AsyncClient) -> None:
    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer INVALID_TOKEN"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_all_sponsors_success(async_client: AsyncClient) -> None:
    # Arrange

    created = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )

    assert created.status_code == 201
    print(created)
    sponsor_id = created.json()["sponsor"]["id"]

    # Act
    response = await async_client.get(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "sponsors" in response_body
    assert isinstance(response_body["sponsors"], list)
    assert any(sponsor["id"] == sponsor_id for sponsor in response_body["sponsors"])

    # Cleanup
    await _delete_sponsor(async_client, sponsor_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_sponsor_by_id_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )
    assert created.status_code == 201
    sponsor = created.json()["sponsor"]
    sponsor_id = sponsor["id"]

    # Act
    response = await async_client.get(
        url=f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "sponsor" in response_body
    assert response_body["sponsor"]["id"] == sponsor_id
    assert response_body["sponsor"]["name"] == sponsor["name"]
    assert response_body["sponsor"]["tier"] == sponsor["tier"]
    assert response_body["sponsor"]["website_url"] == sponsor["website_url"]
    assert response_body["sponsor"]["logo_url"] == sponsor["logo_url"]

    # Cleanup
    await _delete_sponsor(async_client, sponsor_id)


# Error handling is incorrect in impl - error isn't an instance of anything and it goes to default error
@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_sponsor_by_id_invalid_format(async_client: AsyncClient) -> None:
    response = await async_client.get(
        url=f"{SPONSORS_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_sponsor_by_id_not_found(async_client: AsyncClient) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"  # Valid ObjectId, but does belong to an object in the DB

    # Act
    response = await async_client.get(
        url=f"{SPONSORS_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified sponsor was not found"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_update_sponsor_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )
    assert created.status_code == 201
    sponsor_id = created.json()["sponsor"]["id"]

    update_data = {
        "name": "Coca-Cola HBC",
        "website_url": "https://coca-cola.bg/",
    }

    # Act
    response = await async_client.patch(
        url=f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "sponsor" in response_body
    assert response_body["sponsor"]["id"] == sponsor_id
    assert response_body["sponsor"]["name"] == "Coca-Cola HBC"
    assert response_body["sponsor"]["website_url"] == "https://coca-cola.bg/"

    # Cleanup
    await _delete_sponsor(async_client, sponsor_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_delete_sponsor_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=SPONSORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_sponsor_body,
        follow_redirects=True,
    )
    assert created.status_code == 201
    sponsor_id = created.json()["sponsor"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert - Make sure the correct event is deleted
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["sponsor"]["id"] == sponsor_id

    # Assert - Make sure that the event no longer exists
    get_deleted_sponsor = await async_client.get(
        url=f"{SPONSORS_ENDPOINT_URL}/{sponsor_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )
    assert get_deleted_sponsor.status_code == 404
