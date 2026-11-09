from typing import Any

import pytest
from httpx import AsyncClient

ATTENDEES_ENDPOINT_URL = "/api/v3/attendees"

TEST_ATTENDEE_NAME = "John Doe"
TEST_ATTENDEE_EMAIL = "john.doe@gmail.com"
TEST_ATTENDEE_HAS_PAID = True
TEST_ATTENDEE_TICKET_TYPE = "GUEST"
TEST_ATTENDEE_TICKET_SERIAL_NUMBER = "serial-123"

valid_attendee_input: dict[str, Any] = {
    "name": TEST_ATTENDEE_NAME,
    "email": TEST_ATTENDEE_EMAIL,
    "has_paid": TEST_ATTENDEE_HAS_PAID,
    "ticket_type": TEST_ATTENDEE_TICKET_TYPE,
}


async def _delete_attendee(async_client: AsyncClient, attendee_id: str, super_auth_token: str) -> None:
    await async_client.delete(
        url=f"{ATTENDEES_ENDPOINT_URL}/{attendee_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )


@pytest.mark.asyncio
async def test_create_attendee_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_attendee_input,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "attendee" in response_body
    assert response_body["attendee"]["name"] == TEST_ATTENDEE_NAME
    assert response_body["attendee"]["email"] == TEST_ATTENDEE_EMAIL
    assert response_body["attendee"]["has_paid"] == TEST_ATTENDEE_HAS_PAID
    assert response_body["attendee"]["ticket_type"] == TEST_ATTENDEE_TICKET_TYPE
    assert "ticket_serial_number" in response_body["attendee"]
    assert "id" in response_body["attendee"]

    # Cleanup
    attendee_id = response_body["attendee"]["id"]
    await _delete_attendee(async_client, attendee_id, super_auth_token)


@pytest.mark.asyncio
async def test_create_attendee_missing_parameter(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    invalid_attendee_body: dict[str, Any] = {
        "name": TEST_ATTENDEE_NAME,
        "email": TEST_ATTENDEE_EMAIL,
        "has_paid": TEST_ATTENDEE_HAS_PAID,
    }

    # Act
    response = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=invalid_attendee_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()

    assert response_body["detail"][0]["type"] == "missing"
    assert "ticket_type" in response_body["detail"][0]["loc"]


# @pytest.mark.asyncio
# async def test_create_attendee_unauthorized(
#     async_client: AsyncClient
# ) -> None:
#     # Arrange - No new object needed
#
#     # Act
#     response = await async_client.post(
#         url=ATTENDEES_ENDPOINT_URL,
#         headers={"Authorization": f"Bearer INVALID_TOKEN"},
#         json=valid_attendee_input,
#         follow_redirects=True,
#     )
#
#     # Assert
#     assert response.status_code == 401
#     assert response.json()["error"] == "Unauthorized"


@pytest.mark.asyncio
async def test_get_all_attendees_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange

    created = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_attendee_input,
        follow_redirects=True,
    )

    assert created.status_code == 201
    attendee_id = created.json()["attendee"]["id"]

    # Act
    response = await async_client.get(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "attendees" in response_body
    assert isinstance(response_body["attendees"], list)
    assert any(attendee["id"] == attendee_id for attendee in response_body["attendees"])

    # Cleanup
    await _delete_attendee(async_client, attendee_id, super_auth_token)


@pytest.mark.asyncio
async def test_get_attendee_by_id_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_attendee_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    attendee = created.json()["attendee"]
    attendee_id = attendee["id"]

    # Act
    response = await async_client.get(
        url=f"{ATTENDEES_ENDPOINT_URL}/{attendee_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "attendee" in response_body
    assert response_body["attendee"]["id"] == attendee_id
    assert response_body["attendee"]["name"] == attendee["name"]
    assert response_body["attendee"]["email"] == attendee["email"]
    assert response_body["attendee"]["has_paid"] == attendee["has_paid"]
    assert response_body["attendee"]["ticket_type"] == attendee["ticket_type"]
    assert response_body["attendee"]["ticket_serial_number"] == attendee["ticket_serial_number"]

    # Cleanup
    await _delete_attendee(async_client, attendee_id, super_auth_token)


# Error handling is incorrect in impl - error isn't an instance of anything and it goes to default error
@pytest.mark.asyncio
async def test_get_attendee_by_id_invalid_format(async_client: AsyncClient, super_auth_token: str) -> None:
    response = await async_client.get(
        url=f"{ATTENDEES_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@pytest.mark.asyncio
async def test_get_attendee_by_id_not_found(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"  # Valid ObjectId, but does belong to an object in the DB

    # Act
    response = await async_client.get(
        url=f"{ATTENDEES_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified attendee was not found"


@pytest.mark.asyncio
async def test_update_attendee_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_attendee_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    attendee_id = created.json()["attendee"]["id"]

    update_data: dict[str, Any] = {
        "name": "Josh Doe",
        "email": "josh.doe@gmail.com",
    }

    # Act
    response = await async_client.patch(
        url=f"{ATTENDEES_ENDPOINT_URL}/{attendee_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "attendee" in response_body
    assert response_body["attendee"]["id"] == attendee_id
    assert response_body["attendee"]["name"] == "Josh Doe"
    assert response_body["attendee"]["email"] == "josh.doe@gmail.com"

    # Cleanup
    await _delete_attendee(async_client, attendee_id, super_auth_token)


@pytest.mark.asyncio
async def test_delete_attendee_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=ATTENDEES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_attendee_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    attendee_id = created.json()["attendee"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{ATTENDEES_ENDPOINT_URL}/{attendee_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert - Make sure the correct event is deleted
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["attendee"]["id"] == attendee_id

    # Assert - Make sure that the event no longer exists
    get_deleted_attendee = await async_client.get(
        url=f"{ATTENDEES_ENDPOINT_URL}/{attendee_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )
    assert get_deleted_attendee.status_code == 404
