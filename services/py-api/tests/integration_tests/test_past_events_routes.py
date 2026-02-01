from os import environ
from unittest.mock import patch
from typing import Any

import pytest
from httpx import AsyncClient

PAST_EVENTS_ENDPOINT_URL = "/api/v3/admin/events"


def _valid_past_event_payload() -> dict[str, Any]:
    return {
        "title": "HubConf 2024",
        "cover_picture": "https://example.com/hubconf.jpg",
        "tags": ["conference", "hub"],
    }


async def _delete_past_event(async_client: AsyncClient, past_event_id: str) -> None:
    await async_client.delete(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{past_event_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_create_past_event_success(async_client: AsyncClient) -> None:
    # When
    result = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )

    # Then
    assert result.status_code == 201
    body = result.json()

    assert "past_event" in body
    assert body["past_event"]["title"] == "HubConf 2024"
    assert body["past_event"]["cover_picture"] == "https://example.com/hubconf.jpg"
    assert body["past_event"]["tags"] == ["conference", "hub"]
    assert "id" in body["past_event"]

    # Cleanup
    await _delete_past_event(async_client=async_client, past_event_id=body["past_event"]["id"])


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_create_past_event_unauthorized(async_client: AsyncClient) -> None:
    result = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": "Bearer WRONG_TOKEN"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )

    assert result.status_code == 401
    assert result.json()["error"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_all_past_events_success(async_client: AsyncClient) -> None:
    # Arrange: create one event so the list has a stable target
    created = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["past_event"]["id"]

    # Act: list all
    result = await async_client.get(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()

    assert "past_events" in body
    assert isinstance(body["past_events"], list)
    assert any(e["id"] == created_id for e in body["past_events"])

    # Cleanup
    await _delete_past_event(async_client=async_client, past_event_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_past_event_by_id_success(async_client: AsyncClient) -> None:
    # Arrange: create an event
    created = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_event = created.json()["past_event"]
    created_id = created_event["id"]

    # Act: fetch by id
    result = await async_client.get(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()
    assert "past_event" in body
    assert body["past_event"]["id"] == created_id
    assert body["past_event"]["title"] == created_event["title"]
    assert body["past_event"]["cover_picture"] == created_event["cover_picture"]
    assert body["past_event"]["tags"] == created_event["tags"]

    # Cleanup
    await _delete_past_event(async_client=async_client, past_event_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_past_event_by_id_invalid_format(async_client: AsyncClient) -> None:
    result = await async_client.get(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/not-a-valid-object-id",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert result.status_code == 400
    assert result.json()["error"] == "Wrong Object ID format"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_get_past_event_by_id_not_found(async_client: AsyncClient) -> None:
    non_existing_id = "507f1f77bcf86cd799439011"  # valid ObjectId, but not in DB

    result = await async_client.get(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{non_existing_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert result.status_code == 404
    assert result.json()["error"] == "The specified past event was not found"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_update_past_event_success(async_client: AsyncClient) -> None:
    # Arrange: create one event
    created = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["past_event"]["id"]

    update_payload = {
        "title": "HubConf 2024 Updated",
        "cover_picture": "https://example.com/hubconf-updated.jpg",
        "tags": ["conference", "updated"],
    }

    # Act: update
    result = await async_client.patch(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=update_payload,
        follow_redirects=True,
    )

    # Assert
    assert result.status_code == 200
    body = result.json()
    assert "past_event" in body
    assert body["past_event"]["id"] == created_id
    assert body["past_event"]["title"] == "HubConf 2024 Updated"
    assert body["past_event"]["cover_picture"] == "https://example.com/hubconf-updated.jpg"
    assert body["past_event"]["tags"] == ["conference", "updated"]

    # Cleanup
    await _delete_past_event(async_client=async_client, past_event_id=created_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_past_event_success(async_client: AsyncClient) -> None:
    # Arrange: create one event
    created = await async_client.post(
        url=PAST_EVENTS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=_valid_past_event_payload(),
        follow_redirects=True,
    )
    assert created.status_code == 201
    created_id = created.json()["past_event"]["id"]

    # Act: delete
    result = await async_client.delete(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert: delete returns the deleted event
    assert result.status_code == 200
    body = result.json()
    assert body["past_event"]["id"] == created_id

    # Assert: the event is actually gone
    get_after_delete = await async_client.get(
        url=f"{PAST_EVENTS_ENDPOINT_URL}/{created_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )
    assert get_after_delete.status_code == 404
