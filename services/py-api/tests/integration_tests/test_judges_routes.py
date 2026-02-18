from typing import Any
from os import environ
from unittest.mock import patch
import pytest
from httpx import AsyncClient

JUDGES_ENDPOINT_URL = "/api/v3/admin/judges"

TEST_JUDGE_NAME = "Dimitrichko"
TEST_JUDGE_COMPANY = "The Hub"
TEST_JUDGE_AVATAR_URL = "https://eu.aws.com/coca-cola.jpg"
TEST_JUDGE_JOB_TITLE = "Coder"
TEST_JUDGE_LINKEDIN_URL = "https://example.com"

valid_judge_body: dict[str, Any] = {
    "name": TEST_JUDGE_NAME,
    "company": TEST_JUDGE_COMPANY,
    "job_title": TEST_JUDGE_JOB_TITLE,
    "avatar_url": str(TEST_JUDGE_AVATAR_URL),
    "linkedin_url": TEST_JUDGE_LINKEDIN_URL,
}


async def _delete_judge(async_client: AsyncClient, judge_id: str) -> None:
    await async_client.delete(
        url=f"{JUDGES_ENDPOINT_URL}/{judge_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_judge_success(async_client: AsyncClient) -> None:
    # Act
    response = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_judge_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "judge" in response_body
    assert response_body["judge"]["name"] == TEST_JUDGE_NAME
    assert response_body["judge"]["company"] == TEST_JUDGE_COMPANY
    assert response_body["judge"]["job_title"] == TEST_JUDGE_JOB_TITLE
    assert response_body["judge"]["avatar_url"] == TEST_JUDGE_AVATAR_URL
    assert "id" in response_body["judge"]

    # Cleanup
    judge_id = response_body["judge"]["id"]
    await _delete_judge(async_client, judge_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_judge_missing_parameter(async_client: AsyncClient) -> None:
    # Arrange - Missing avatar_url
    invalid_judge_body: dict[str, Any] = {
        "name": TEST_JUDGE_NAME,
        "company": TEST_JUDGE_COMPANY,
        "job_title": TEST_JUDGE_JOB_TITLE,
    }

    # Act
    response = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=invalid_judge_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"][0]["type"] == "missing"
    assert "avatar_url" in response_body["detail"][0]["loc"]


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_create_judge_unauthorized(async_client: AsyncClient) -> None:
    # Act
    response = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer INVALID_TOKEN"},
        json=valid_judge_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_all_judges_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_judge_body,
        follow_redirects=True,
    )
    judge_id = created.json()["judge"]["id"]

    # Act
    response = await async_client.get(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "judges" in response_body
    assert isinstance(response_body["judges"], list)
    assert any(j["id"] == judge_id for j in response_body["judges"])

    # Cleanup
    await _delete_judge(async_client, judge_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_judge_by_id_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_judge_body,
        follow_redirects=True,
    )
    judge = created.json()["judge"]
    judge_id = judge["id"]

    # Act
    response = await async_client.get(
        url=f"{JUDGES_ENDPOINT_URL}/{judge_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["judge"]["id"] == judge_id
    assert response_body["judge"]["name"] == judge["name"]
    assert response_body["judge"]["company"] == judge["company"]

    # Cleanup
    await _delete_judge(async_client, judge_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_judge_by_id_invalid_format(async_client: AsyncClient) -> None:
    response = await async_client.get(
        url=f"{JUDGES_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_get_judge_by_id_not_found(async_client: AsyncClient) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"

    # Act
    response = await async_client.get(
        url=f"{JUDGES_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified judge was not found"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_update_judge_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_judge_body,
        follow_redirects=True,
    )
    judge_id = created.json()["judge"]["id"]

    update_data = {
        "name": "Updated Dimitrichko",
        "job_title": "Senior Coder",
    }

    # Act
    response = await async_client.patch(
        url=f"{JUDGES_ENDPOINT_URL}/{judge_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["judge"]["name"] == "Updated Dimitrichko"
    assert response_body["judge"]["job_title"] == "Senior Coder"

    # Cleanup
    await _delete_judge(async_client, judge_id)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "TEST_TOKEN"})
@pytest.mark.asyncio
async def test_delete_judge_success(async_client: AsyncClient) -> None:
    # Arrange
    created = await async_client.post(
        url=JUDGES_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        json=valid_judge_body,
        follow_redirects=True,
    )
    judge_id = created.json()["judge"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{JUDGES_ENDPOINT_URL}/{judge_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["judge"]["id"] == judge_id

    # Verify 404
    get_deleted = await async_client.get(
        url=f"{JUDGES_ENDPOINT_URL}/{judge_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert get_deleted.status_code == 404
