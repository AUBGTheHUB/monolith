from os import environ
from unittest.mock import patch

from httpx import AsyncClient
import pytest
from tests.integration_tests.conftest import (
    TEAM_ENDPOINT_URL,
    TEST_TEAM_NAME,
    CreateTestParticipantCallable,
    ParticipantRequestBodyCallable,
)


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_delete_team_success(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    async_client: AsyncClient,
) -> None:

    # The only way you can create a team currently is through the creation of an admin participant
    # Given
    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    result_1 = await create_test_participant(participant_body=admin_participant_body)

    # When
    result_2 = await async_client.delete(
        url=f"{TEAM_ENDPOINT_URL}/{result_1.json()["team"]["id"]}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    # Then
    assert result_2.status_code == 200

    result_1_json = result_1.json()
    result_2_json = result_2.json()
    assert result_2_json["team"]["id"] == result_1_json["team"]["id"]
    assert result_2_json["team"]["name"] == result_1_json["team"]["name"]
    assert result_2_json["team"]["is_verified"] == result_1_json["team"]["is_verified"]


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_delete_team_unauthorized(async_client: AsyncClient, obj_id_mock: str) -> None:

    # When
    result = await async_client.delete(
        url=f"{TEAM_ENDPOINT_URL}/{obj_id_mock}", headers={"Authorization": "Bearer FakeToken"}
    )

    # Then
    assert result.status_code == 401
    assert result.json()["error"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_team_wrong_obj_id_format(async_client: AsyncClient) -> None:

    # When
    result = await async_client.delete(
        url=f"{TEAM_ENDPOINT_URL}/1", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}
    )

    # Then
    assert result.status_code == 400
    assert result.json()["error"] == "Wrong Object ID format"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_delete_team_obj_id_doesnt_exist(async_client: AsyncClient, obj_id_mock: str) -> None:

    # When
    result = await async_client.delete(
        url=f"{TEAM_ENDPOINT_URL}/{obj_id_mock}", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}
    )

    # Then
    assert result.status_code == 404
    assert result.json()["error"] == "The specified team was not found"
