from os import environ
from unittest.mock import patch
import pytest
from httpx import AsyncClient

from tests.integration_tests.conftest import async_client

DEPARTMENT_MEMBERS_ENDPOINT_URL = "/api/v3/admin/department-members"

TEST_MEMBER_NAME = "Test Member"
TEST_PHOTO_URL = "https://example.com/photo.jpg"
TEST_LINKEDIN_URL = "https://www.linkedin.com/in/test-member"
TEST_DEPARTMENTS = ["Development", "Marketing"]


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_create_department_member_success(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    auth_header = {"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}

    # When
    response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers=auth_header,
    )

    # Then
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["name"] == TEST_MEMBER_NAME
    assert response_json["photo_url"] == TEST_PHOTO_URL
    assert response_json["linkedin_url"] == TEST_LINKEDIN_URL
    assert response_json["departments"] == TEST_DEPARTMENTS
    assert "id" in response_json

    # Cleanup
    member_id = response_json["id"]
    auth_header = {"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}", headers=auth_header)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_create_department_member_invalid_linkedin_url(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": "https://invalid-url.com/in/test",
        "departments": TEST_DEPARTMENTS,
    }

    # When
    response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_create_department_member_missing_fields(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
    }

    # When
    response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_create_department_member_unauthorized(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }

    # When
    response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
    )

    # Then
    assert response.status_code == 401


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_get_all_department_members_success(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    created_member_id = create_response.json()["id"]

    # When
    response = await async_client.get(DEPARTMENT_MEMBERS_ENDPOINT_URL, headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert "members" in response_json
    assert isinstance(response_json["members"], list)
    assert len(response_json["members"]) > 0
    member_ids = [m["id"] for m in response_json["members"]]
    assert created_member_id in member_ids

    # Cleanup
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{created_member_id}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_get_department_member_by_id_success(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # When
    response = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == member_id
    assert response_json["name"] == TEST_MEMBER_NAME
    assert response_json["photo_url"] == TEST_PHOTO_URL
    assert response_json["linkedin_url"] == TEST_LINKEDIN_URL
    assert response_json["departments"] == TEST_DEPARTMENTS

    # Cleanup
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_get_department_member_by_id_not_found(async_client: AsyncClient) -> None:
    # Given
    non_existent_id = "507f1f77bcf86cd799439011"

    # When
    response = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{non_existent_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 404
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_get_department_member_by_id_invalid_object_id(async_client: AsyncClient) -> None:
    # Given
    invalid_id = "invalid-id"

    # When
    response = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{invalid_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_update_department_member_success(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # When
    update_body = {
        "name": "Updated Member Name",
        "departments": ["Development"],
    }
    response = await async_client.patch(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        json=update_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == member_id
    assert response_json["name"] == "Updated Member Name"
    assert response_json["departments"] == ["Development"]
    assert response_json["photo_url"] == TEST_PHOTO_URL
    assert response_json["linkedin_url"] == TEST_LINKEDIN_URL

    # Cleanup
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_update_department_member_partial_update(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # When
    update_body = {
        "name": "Only Name Updated",
    }
    response = await async_client.patch(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        json=update_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "Only Name Updated"
    assert response_json["photo_url"] == TEST_PHOTO_URL
    assert response_json["linkedin_url"] == TEST_LINKEDIN_URL
    assert response_json["departments"] == TEST_DEPARTMENTS

    # Cleanup
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_update_department_member_invalid_linkedin_url(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # When
    update_body = {
        "linkedin_url": "https://invalid-url.com/in/test",
    }
    response = await async_client.patch(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        json=update_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json

    # Cleanup
    await async_client.delete(f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_update_department_member_not_found(async_client: AsyncClient) -> None:
    # Given
    non_existent_id = "507f1f77bcf86cd799439011"
    update_body = {
        "name": "Updated Name",
    }

    # When
    response = await async_client.patch(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{non_existent_id}",
        json=update_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 404
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_delete_department_member_success(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # When
    response = await async_client.delete(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == member_id
    assert response_json["name"] == TEST_MEMBER_NAME

    # Verify deletion
    get_response = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert get_response.status_code == 404


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_delete_department_member_not_found(async_client: AsyncClient) -> None:
    # Given
    non_existent_id = "507f1f77bcf86cd799439011"

    # When
    response = await async_client.delete(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{non_existent_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 404
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_delete_department_member_invalid_object_id(async_client: AsyncClient) -> None:
    # Given
    invalid_id = "invalid-id"

    # When
    response = await async_client.delete(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{invalid_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "test-token"})
@pytest.mark.asyncio
async def test_department_members_crud_full_flow(async_client: AsyncClient) -> None:
    # Given
    member_body = {
        "name": TEST_MEMBER_NAME,
        "photo_url": TEST_PHOTO_URL,
        "linkedin_url": TEST_LINKEDIN_URL,
        "departments": TEST_DEPARTMENTS,
    }

    # Create
    create_response = await async_client.post(
        DEPARTMENT_MEMBERS_ENDPOINT_URL,
        json=member_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert create_response.status_code == 201
    member_id = create_response.json()["id"]

    # List all
    list_response = await async_client.get(DEPARTMENT_MEMBERS_ENDPOINT_URL, headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"})
    assert list_response.status_code == 200
    member_ids = [m["id"] for m in list_response.json()["members"]]
    assert member_id in member_ids

    # Get by ID
    get_response = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert get_response.status_code == 200
    assert get_response.json()["id"] == member_id

    # Update
    update_body = {"name": "Updated Name", "departments": ["Development"]}
    update_response = await async_client.patch(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        json=update_body,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Name"

    # Delete
    delete_response = await async_client.delete(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert delete_response.status_code == 200

    # Verify deleted
    get_after_delete = await async_client.get(
        f"{DEPARTMENT_MEMBERS_ENDPOINT_URL}/{member_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert get_after_delete.status_code == 404

