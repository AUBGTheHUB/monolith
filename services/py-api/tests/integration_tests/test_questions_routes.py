from typing import Any

import pytest
from httpx import AsyncClient

QUESTIONS_ENDPOINT_URL = "/api/v3/questions"

TEST_QUESTION_PROMPT = "How are you?"
TEST_QUESTION_TYPE = "DEVELOPMENT"
TEST_ANSWER_TYPE = "TEXT"
TEST_ANSWER = "Very good"
TEST_QUESTION_OPTIONS = None

valid_question_input: dict[str, Any] = {
    "prompt": TEST_QUESTION_PROMPT,
    "question_type": TEST_QUESTION_TYPE,
    "answer_type": TEST_ANSWER_TYPE,
}


async def _delete_question(async_client: AsyncClient, question_id: str, super_auth_token: str) -> None:
    await async_client.delete(
        url=f"{QUESTIONS_ENDPOINT_URL}/{question_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )


@pytest.mark.asyncio
async def test_create_question_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_question_input,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "question" in response_body
    assert response_body["question"]["prompt"] == TEST_QUESTION_PROMPT
    assert response_body["question"]["question_type"] == TEST_QUESTION_TYPE
    assert response_body["question"]["answer_type"] == TEST_ANSWER_TYPE
    assert "id" in response_body["question"]

    # Cleanup
    question_id = response_body["question"]["id"]
    await _delete_question(async_client, question_id, super_auth_token)


@pytest.mark.asyncio
async def test_create_question_missing_parameter(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    invalid_question_body: dict[str, Any] = {
        "prompt": TEST_QUESTION_PROMPT,
        "question_type": TEST_QUESTION_TYPE,
    }

    # Act
    response = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=invalid_question_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()

    assert response_body["detail"][0]["type"] == "missing"
    assert "answer_type" in response_body["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_create_question_unauthorized(async_client: AsyncClient) -> None:
    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer INVALID_TOKEN"},
        json=valid_question_input,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"


@pytest.mark.asyncio
async def test_get_all_questions_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange

    created = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_question_input,
        follow_redirects=True,
    )

    assert created.status_code == 201
    question_id = created.json()["question"]["id"]

    # Act
    response = await async_client.get(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "questions" in response_body
    assert isinstance(response_body["questions"], list)
    assert any(question["id"] == question_id for question in response_body["questions"])

    # Cleanup
    await _delete_question(async_client, question_id, super_auth_token)


@pytest.mark.asyncio
async def test_get_question_by_id_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_question_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    question = created.json()["question"]
    question_id = question["id"]

    # Act
    response = await async_client.get(
        url=f"{QUESTIONS_ENDPOINT_URL}/{question_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "question" in response_body
    assert response_body["question"]["id"] == question_id
    assert response_body["question"]["prompt"] == question["prompt"]
    assert response_body["question"]["question_type"] == question["question_type"]
    assert response_body["question"]["answer_type"] == question["answer_type"]

    # Cleanup
    await _delete_question(async_client, question_id, super_auth_token)


# Error handling is incorrect in impl - error isn't an instance of anything and it goes to default error
@pytest.mark.asyncio
async def test_get_question_by_id_invalid_format(async_client: AsyncClient, super_auth_token: str) -> None:
    response = await async_client.get(
        url=f"{QUESTIONS_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@pytest.mark.asyncio
async def test_get_question_by_id_not_found(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"  # Valid ObjectId, but does belong to an object in the DB

    # Act
    response = await async_client.get(
        url=f"{QUESTIONS_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified question was not found"


@pytest.mark.asyncio
async def test_update_question_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_question_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    question_id = created.json()["question"]["id"]

    update_data: dict[str, Any] = {
        "prompt": "Updated question",
    }

    # Act
    response = await async_client.patch(
        url=f"{QUESTIONS_ENDPOINT_URL}/{question_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "question" in response_body
    assert response_body["question"]["id"] == question_id
    assert response_body["question"]["prompt"] == "Updated question"

    # Cleanup
    await _delete_question(async_client, question_id, super_auth_token)


@pytest.mark.asyncio
async def test_delete_question_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=QUESTIONS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_question_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    question_id = created.json()["question"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{QUESTIONS_ENDPOINT_URL}/{question_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert - Make sure the correct event is deleted
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["question"]["id"] == question_id

    # Assert - Make sure that the event no longer exists
    get_deleted_question = await async_client.get(
        url=f"{QUESTIONS_ENDPOINT_URL}/{question_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )
    assert get_deleted_question.status_code == 404
