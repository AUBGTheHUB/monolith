import pytest
from typing import Any, Callable, Dict
from httpx import AsyncClient

from src.utils import JwtUtility
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData
from tests.integration_tests.conftest import PARTICIPANT_ENDPOINT_URL

EXPIRED_TOKEN_DATE = 1235641475.917655
VALID_TOKEN_DATE = 8035641475.917655


# The source of information for the request is the jwt token, so each test would need an appropriate one
def generate_appropriate_token(sub: str, is_admin: bool, team_id: str, exp: float) -> str:
    return JwtUtility.encode_data(data=JwtUserData(sub=sub, is_admin=is_admin, team_id=team_id, exp=exp))


@pytest.mark.asyncio
async def test_verify_participant_admin_case_success(
    generate_participant_request_body: Callable[..., Dict[str, Any]],
    create_test_participant: Callable[..., Dict[str, Any]],
    async_client: AsyncClient,
) -> None:

    admin_participant_body = generate_participant_request_body(is_admin=True, team_name="test")
    res_one = await create_test_participant(participant_body=admin_participant_body)
    res_one_json = res_one.json()

    jwt = generate_appropriate_token(
        res_one_json["participant"]["id"], True, res_one_json["team"]["id"], VALID_TOKEN_DATE
    )

    res_two = await async_client.patch(url=f"{PARTICIPANT_ENDPOINT_URL}/verify?jwt_token={jwt}")

    res_two_json = res_two.json()

    assert res_two.status_code == 200

    assert res_two_json["team"]["id"] == res_one_json["team"]["id"]
    assert res_two_json["participant"]["id"] == res_one_json["participant"]["id"]
    assert res_two_json["team"]["is_verified"] is True
    assert res_two_json["participant"]["email_verified"] is True


@pytest.mark.asyncio
async def test_verify_participant_admin_case_when_participant_is_not_found(
    generate_participant_request_body: Callable[..., Dict[str, Any]],
    create_test_participant: Callable[..., Dict[str, Any]],
    mock_obj_id: str,
    async_client: AsyncClient,
) -> None:

    # we need an existing team_id for the token and the only way to create a team is to create an admin participant as well
    admin_participant_body = generate_participant_request_body(is_admin=True, team_name="test")
    res_one = await create_test_participant(participant_body=admin_participant_body)

    # token with existing team_id but not existing participant_id (sub)
    jwt = generate_appropriate_token(mock_obj_id, True, res_one.json()["team"]["id"], VALID_TOKEN_DATE)

    res_two = await async_client.patch(url=f"{PARTICIPANT_ENDPOINT_URL}/verify?jwt_token={jwt}")

    assert res_two.status_code == 404
    assert res_two.json()["error"] == "The participant was not found"


@pytest.mark.asyncio
async def test_verify_participant_admin_case_when_team_is_not_found(
    generate_participant_request_body: Callable[..., Dict[str, Any]],
    create_test_participant: Callable[..., Dict[str, Any]],
    mock_obj_id: str,
    async_client: AsyncClient,
) -> None:

    # we need an existing participant_id for the token so we generate an admin participant
    admin_participant_body = generate_participant_request_body(is_admin=True, team_name="test")
    res_one = await create_test_participant(participant_body=admin_participant_body)

    # token with existing participant_id (sub) but not existing team_id
    jwt = generate_appropriate_token(res_one.json()["participant"]["id"], True, mock_obj_id, VALID_TOKEN_DATE)

    res_two = await async_client.patch(url=f"{PARTICIPANT_ENDPOINT_URL}/verify?jwt_token={jwt}")

    res_two_json = res_two.json()
    assert res_two.status_code == 404
    assert res_two_json["error"] == "The team was not found"


@pytest.mark.asyncio
async def test_verify_participant_admin_case_expired_token(
    generate_participant_request_body: Callable[..., Dict[str, Any]],
    create_test_participant: Callable[..., Dict[str, Any]],
    async_client: AsyncClient,
) -> None:

    # We would like to have existing participant_id and team_id for the token
    admin_participant_body = generate_participant_request_body(is_admin=True, team_name="test")
    res_one = await create_test_participant(participant_body=admin_participant_body)
    res_one_json = res_one.json()

    # token with existing participant_id (sub) and team_id but with passed expiration date
    jwt = generate_appropriate_token(
        res_one_json["participant"]["id"], True, res_one_json["team"]["id"], EXPIRED_TOKEN_DATE
    )

    invalid_token_result = await async_client.patch(url=f"{PARTICIPANT_ENDPOINT_URL}/verify?jwt_token={jwt}")

    assert invalid_token_result.status_code == 400
    assert invalid_token_result.json()["error"] == "The JWT token has expired."


@pytest.mark.asyncio
async def test_verify_participant_admin_case_invalid_token(
    async_client: AsyncClient,
) -> None:

    fake_token_result = await async_client.patch(url=f"{PARTICIPANT_ENDPOINT_URL}/verify?jwt_token=FAKE_TOKEN")

    assert fake_token_result.status_code == 400
