from os import environ
from unittest.mock import patch
from typing import Any

import pytest
from httpx import AsyncClient

HUB_MEMBERS_ENDPOINT_URL = "/api/v3/admin/hub-members"


def _valid_hub_member_payload() -> dict[str, Any]:
    return {
        "name": "John Doe",
        "position": "Senior Developer",
        "department": "Development",
        "avatar_url": "https://example.com/avatar.jpg",
        "social_links": {
            "linkedin": "https://www.linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe",
        },
    }


async def _delete_hub_member(async_client: AsyncClient, member_id: str) -> None:
    await async_client.delete(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_create_hub_member_success(async_client: AsyncClient) -> None:
    # When
    result = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )

    # Then
    assert result.status_code == 201
    body = result.json()

    assert "hub_member" in body
    assert body["hub_member"]["name"] == "John Doe"
    assert body["hub_member"]["position"] == "Senior Developer"
    assert body["hub_member"]["department"] == "Development"
    assert body["hub_member"]["avatar_url"] == "https://example.com/avatar.jpg"
    assert "id" in body["hub_member"]

    # Cleanup
    await _delete_hub_member(async_client=async_client, member_id=body["hub_member"]["id"])


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_create_hub_member_unauthorized(async_client: AsyncClient) -> None:
    result = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": "Bearer WRONG_TOKEN"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )

    assert result.status_code == 401
    assert result.json()["error"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_all_hub_members_success(async_client: AsyncClient) -> None:
    # Arrange: create one member so the list has a stable target
    created = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["hub_member"]["id"]

    # Act: list all
    result = await async_client.get(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()

    assert "members" in body
    assert isinstance(body["members"], list)
    assert any(m["id"] == created_id for m in body["members"])

    # Cleanup
    await _delete_hub_member(async_client=async_client, member_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_hub_member_by_id_success(async_client: AsyncClient) -> None:
    # Arrange: create a member
    created = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_member = created.json()["hub_member"]
    created_id = created_member["id"]

    # Act: fetch by id
    result = await async_client.get(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()
    assert "hub_member" in body
    assert body["hub_member"]["id"] == created_id
    assert body["hub_member"]["name"] == created_member["name"]
    assert body["hub_member"]["position"] == created_member["position"]
    assert body["hub_member"]["department"] == created_member["department"]

    # Cleanup
    await _delete_hub_member(async_client=async_client, member_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_hub_member_by_id_invalid_format(async_client: AsyncClient) -> None:
    result = await async_client.get(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/not-a-valid-object-id",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert result.status_code == 400


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_hub_member_by_id_not_found(async_client: AsyncClient) -> None:
    non_existing_id = "507f1f77bcf86cd799439011"  # valid ObjectId, but not in DB

    result = await async_client.get(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{non_existing_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert result.status_code == 404
    assert result.json()["error"] == "The hub member was not found."


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_update_hub_member_success(async_client: AsyncClient) -> None:
    # Arrange: create one member
    created = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["hub_member"]["id"]

    update_payload = {
        "name": "Jane Doe",
        "position": "Lead Developer",
        "department": "Development",
    }

    # Act: update
    result = await async_client.patch(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=update_payload,
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()
    assert "hub_member" in body
    assert body["hub_member"]["id"] == created_id
    assert body["hub_member"]["name"] == "Jane Doe"
    assert body["hub_member"]["position"] == "Lead Developer"

    # Cleanup
    await _delete_hub_member(async_client=async_client, member_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_hub_member_success(async_client: AsyncClient) -> None:
    # Arrange: create one member
    created = await async_client.post(
        url=HUB_MEMBERS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_hub_member_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["hub_member"]["id"]

    # Act: delete
    result = await async_client.delete(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert: delete returns the deleted member
    assert result.status_code == 200
    body = result.json()
    assert body["hub_member"]["id"] == created_id

    # Assert: the member is actually gone
    get_after_delete = await async_client.get(
        url=f"{HUB_MEMBERS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )
    assert get_after_delete.status_code == 404
