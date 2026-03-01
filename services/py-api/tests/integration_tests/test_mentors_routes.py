from io import BytesIO
import pytest
from httpx import AsyncClient
from typing import Any, Generator

from src.environment import AWS_S3_DEFAULT_BUCKET, AWS_DEFAULT_REGION

MENTORS_ENDPOINT_URL = "/api/v3/admin/mentors"

TEST_MENTOR_NAME = "Jane Doe"
TEST_MENTOR_COMPANY = "ACME"
TEST_MENTOR_JOB_TITLE = "Engineer"
TEST_MENTOR_LINKEDIN_URL = "https://linkedin.com/janedoe"

TEST_MENTOR_AVATAR_URL = f"https://{AWS_S3_DEFAULT_BUCKET}.s3.{AWS_DEFAULT_REGION}.amazonaws.com/mentors"

valid_mentor_body: dict[str, Any] = {
    "name": TEST_MENTOR_NAME,
    "company": TEST_MENTOR_COMPANY,
    "job_title": TEST_MENTOR_JOB_TITLE,
    "linkedin_url": TEST_MENTOR_LINKEDIN_URL,
}


async def _delete_mentor(async_client: AsyncClient, mentor_id: str, super_auth_token: str) -> None:
    await async_client.delete(
        url=f"{MENTORS_ENDPOINT_URL}/{mentor_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )


@pytest.mark.asyncio
async def test_create_mentor_success(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None], super_auth_token: str
) -> None:

    # Act
    response = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "mentor" in response_body
    assert response_body["mentor"]["name"] == TEST_MENTOR_NAME
    assert response_body["mentor"]["company"] == TEST_MENTOR_COMPANY
    assert response_body["mentor"]["job_title"] == TEST_MENTOR_JOB_TITLE
    assert response_body["mentor"]["avatar_url"] == f"{TEST_MENTOR_AVATAR_URL}/{response_body['mentor']['id']}.webp"
    assert response_body["mentor"]["linkedin_url"] == TEST_MENTOR_LINKEDIN_URL
    assert "id" in response_body["mentor"]

    # Cleanup
    mentor_id = response_body["mentor"]["id"]
    await _delete_mentor(async_client, mentor_id, super_auth_token)


@pytest.mark.asyncio
async def test_create_mentor_missing_parameter(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    invalid_body = {k: v for k, v in valid_mentor_body.items() if k != "avatar_url"}

    # Act
    response = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=invalid_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()

    assert response_body["detail"][0]["type"] == "missing"
    assert "avatar" in response_body["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_mentor_unauthorized(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None]
) -> None:
    # Act
    response = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer INVALID_TOKEN"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"


@pytest.mark.asyncio
async def test_get_all_mentors_success(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None], super_auth_token: str
) -> None:
    # Arrange
    created = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )

    assert created.status_code == 201
    mentor_id = created.json()["mentor"]["id"]

    # Act
    response = await async_client.get(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "mentors" in response_body
    assert isinstance(response_body["mentors"], list)
    assert any(mentor["id"] == mentor_id for mentor in response_body["mentors"])

    # Cleanup
    await _delete_mentor(async_client, mentor_id, super_auth_token)


@pytest.mark.asyncio
async def test_get_mentor_by_id_success(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None], super_auth_token: str
) -> None:
    # Arrange
    created = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )

    assert created.status_code == 201
    mentor = created.json()["mentor"]
    mentor_id = mentor["id"]

    # Act
    response = await async_client.get(
        url=f"{MENTORS_ENDPOINT_URL}/{mentor_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "mentor" in response_body
    assert response_body["mentor"]["id"] == mentor_id
    assert response_body["mentor"]["name"] == mentor["name"]
    assert response_body["mentor"]["company"] == mentor["company"]
    assert response_body["mentor"]["avatar_url"] == mentor["avatar_url"]
    assert response_body["mentor"]["job_title"] == mentor["job_title"]

    # Cleanup
    await _delete_mentor(async_client, mentor_id, super_auth_token)


@pytest.mark.asyncio
async def test_get_mentor_by_id_invalid_format(async_client: AsyncClient, super_auth_token: str) -> None:
    response = await async_client.get(
        url=f"{MENTORS_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@pytest.mark.asyncio
async def test_get_mentor_by_id_not_found(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"

    # Act
    response = await async_client.get(
        url=f"{MENTORS_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified mentor was not found"


@pytest.mark.asyncio
async def test_update_mentor_success(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None], super_auth_token: str
) -> None:
    # Arrange
    created = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )
    assert created.status_code == 201
    mentor_id = created.json()["mentor"]["id"]

    update_data = {"name": "Jane A. Doe", "company": "ACME Ltd"}

    # Act
    response = await async_client.patch(
        url=f"{MENTORS_ENDPOINT_URL}/{mentor_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "mentor" in response_body
    assert response_body["mentor"]["id"] == mentor_id
    assert response_body["mentor"]["name"] == "Jane A. Doe"
    assert response_body["mentor"]["company"] == "ACME Ltd"

    # Cleanup
    await _delete_mentor(async_client, mentor_id, super_auth_token)


@pytest.mark.asyncio
async def test_delete_mentor_success(
    async_client: AsyncClient, image_mock: BytesIO, aws_mock: Generator[None, Any, None], super_auth_token: str
) -> None:
    # Arrange
    created = await async_client.post(
        url=MENTORS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        data=valid_mentor_body,
        files={"avatar": image_mock},
        follow_redirects=True,
    )
    assert created.status_code == 201
    mentor_id = created.json()["mentor"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{MENTORS_ENDPOINT_URL}/{mentor_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["mentor"]["id"] == mentor_id

    # Ensure deleted
    get_deleted = await async_client.get(
        url=f"{MENTORS_ENDPOINT_URL}/{mentor_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )
    assert get_deleted.status_code == 404
