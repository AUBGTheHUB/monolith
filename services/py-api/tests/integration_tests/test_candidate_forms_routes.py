from typing import Any

import pytest
from httpx import AsyncClient

from src.database.model.admin.candidates_form.question_model import QuestionParams

CANDIDATE_FORMS_ENDPOINT_URL = "/api/v3/candidate-forms"

TEST_QUESTION_PROMPT = "How are you?"
TEST_QUESTION_TYPE = "DEVELOPMENT"
TEST_ANSWER_TYPE = "TEXT"
TEST_ANSWER = "Very good"
TEST_QUESTION_OPTIONS: list[str] = []
TEST_CANDIDATE_FORM_QUESTIONS = [
    QuestionParams(
        prompt=TEST_QUESTION_PROMPT,
        question_type=TEST_QUESTION_TYPE,
        answer_type=TEST_ANSWER_TYPE,
        answer=TEST_ANSWER,
        options=TEST_QUESTION_OPTIONS,
    )
]

valid_candidate_form_input: dict[str, Any] = {
    "questions": [question.model_dump() for question in TEST_CANDIDATE_FORM_QUESTIONS],
}


async def _delete_candidate_form(async_client: AsyncClient, candidate_form_id: str, super_auth_token: str) -> None:
    await async_client.delete(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{candidate_form_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )


@pytest.mark.asyncio
async def test_create_candidate_form_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange - No new object needed

    # Act
    response = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_candidate_form_input,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 201
    response_body = response.json()

    assert "candidate_form" in response_body

    candidate_form = response_body["candidate_form"]
    assert len(candidate_form["questions"]) == len(TEST_CANDIDATE_FORM_QUESTIONS)

    question = candidate_form["questions"][0]

    assert question["prompt"] == TEST_QUESTION_PROMPT
    assert question["question_type"] == TEST_QUESTION_TYPE
    assert question["answer_type"] == TEST_ANSWER_TYPE
    assert question["answer"] == TEST_ANSWER
    assert question["options"] == TEST_QUESTION_OPTIONS
    assert question["id"]

    # Cleanup
    candidate_form_id = response_body["candidate_form"]["id"]
    await _delete_candidate_form(async_client, candidate_form_id, super_auth_token)


@pytest.mark.asyncio
async def test_create_candidate_form_missing_parameter(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    invalid_candidate_form_body: dict[str, Any] = {"some_key": "some_value"}

    # Act
    response = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=invalid_candidate_form_body,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 422
    response_body = response.json()

    assert response_body["detail"][0]["type"] == "missing"
    assert "questions" in response_body["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_get_all_candidate_forms_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange

    created = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_candidate_form_input,
        follow_redirects=True,
    )

    assert created.status_code == 201
    candidate_form_id = created.json()["candidate_form"]["id"]

    # Act
    response = await async_client.get(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "candidate_forms" in response_body
    assert isinstance(response_body["candidate_forms"], list)
    assert any(candidate_form["id"] == candidate_form_id for candidate_form in response_body["candidate_forms"])

    # Cleanup
    await _delete_candidate_form(async_client, candidate_form_id, super_auth_token)


@pytest.mark.asyncio
async def test_get_candidate_form_by_id_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_candidate_form_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    candidate_form = created.json()["candidate_form"]
    candidate_form_id = candidate_form["id"]

    # Act
    response = await async_client.get(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{candidate_form_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()

    assert "candidate_form" in response_body

    candidate_form = response_body["candidate_form"]
    assert len(candidate_form["questions"]) == len(TEST_CANDIDATE_FORM_QUESTIONS)

    question = candidate_form["questions"][0]

    assert question["prompt"] == TEST_QUESTION_PROMPT
    assert question["question_type"] == TEST_QUESTION_TYPE
    assert question["answer_type"] == TEST_ANSWER_TYPE
    assert question["answer"] == TEST_ANSWER
    assert question["options"] == TEST_QUESTION_OPTIONS
    assert question["id"]

    # Cleanup
    await _delete_candidate_form(async_client, candidate_form_id, super_auth_token)


# Error handling is incorrect in impl - error isn't an instance of anything and it goes to default error
@pytest.mark.asyncio
async def test_get_candidate_form_by_id_invalid_format(async_client: AsyncClient, super_auth_token: str) -> None:
    response = await async_client.get(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/invalid_object_id",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Wrong Object ID format"


@pytest.mark.asyncio
async def test_get_candidate_form_by_id_not_found(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    NON_EXISTING_ID = "6975472e436158f65093dbb5"  # Valid ObjectId, but does belong to an object in the DB

    # Act
    response = await async_client.get(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "The specified candidate form was not found"


@pytest.mark.asyncio
async def test_update_candidate_form_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_candidate_form_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    candidate_form_id = created.json()["candidate_form"]["id"]

    update_data: dict[str, Any] = {
        "questions": [
            QuestionParams(
                prompt=TEST_QUESTION_PROMPT,
                question_type=TEST_QUESTION_TYPE,
                answer_type=TEST_ANSWER_TYPE,
                answer="Updated answer",
                options=TEST_QUESTION_OPTIONS,
            ).model_dump()
        ],
    }

    # Act
    response = await async_client.patch(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{candidate_form_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=update_data,
        follow_redirects=True,
    )

    # Assert
    assert response.status_code == 200
    response_body = response.json()
    assert "candidate_form" in response_body
    assert response_body["candidate_form"]["id"] == candidate_form_id

    candidate_form = response_body["candidate_form"]
    assert len(candidate_form["questions"]) == len(TEST_CANDIDATE_FORM_QUESTIONS)

    question = candidate_form["questions"][0]

    assert question["prompt"] == TEST_QUESTION_PROMPT
    assert question["question_type"] == TEST_QUESTION_TYPE
    assert question["answer_type"] == TEST_ANSWER_TYPE
    assert question["answer"] == "Updated answer"
    assert question["options"] == TEST_QUESTION_OPTIONS
    assert question["id"]

    # Cleanup
    await _delete_candidate_form(async_client, candidate_form_id, super_auth_token)


@pytest.mark.asyncio
async def test_delete_candidate_form_success(async_client: AsyncClient, super_auth_token: str) -> None:
    # Arrange
    created = await async_client.post(
        url=CANDIDATE_FORMS_ENDPOINT_URL,
        headers={"Authorization": f"Bearer {super_auth_token}"},
        json=valid_candidate_form_input,
        follow_redirects=True,
    )
    assert created.status_code == 201
    candidate_form_id = created.json()["candidate_form"]["id"]

    # Act
    response = await async_client.delete(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{candidate_form_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )

    # Assert - Make sure the correct event is deleted
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["candidate_form"]["id"] == candidate_form_id

    # Assert - Make sure that the event no longer exists
    get_deleted_candidate_form = await async_client.get(
        url=f"{CANDIDATE_FORMS_ENDPOINT_URL}/{candidate_form_id}",
        headers={"Authorization": f"Bearer {super_auth_token}"},
        follow_redirects=True,
    )
    assert get_deleted_candidate_form.status_code == 404
