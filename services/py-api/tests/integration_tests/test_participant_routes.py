from os import environ
from unittest.mock import patch
from httpx import AsyncClient
import pytest
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserRegistration
from tests.integration_tests.conftest import (
    PARTICIPANT_ENDPOINT_URL,
    TEST_TEAM_NAME,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    ParticipantRequestBodyCallable,
    CreateTestParticipantCallable,
)
from tests.integration_tests.test_jwt_utility import sufficient_expiration_time
from src.database.repository.teams_repository import TeamsRepository
from src.utils import JwtUtility


@pytest.mark.asyncio
async def test_create_random_participant(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    resp = await create_test_participant(participant_body=random_participant_body)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == TEST_USER_NAME
    assert resp_json["participant"]["email"] == TEST_USER_EMAIL
    assert resp_json["participant"]["is_admin"] is False
    assert resp_json["participant"]["email_verified"] is False
    assert resp_json["participant"]["team_id"] is None
    assert resp_json["team"] is None


@pytest.mark.asyncio
async def test_create_random_participant_email_already_exists(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    await create_test_participant(participant_body=random_participant_body)
    resp = await create_test_participant(participant_body=random_participant_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_no_team_name(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    is_admin_true_body = generate_participant_request_body(registration_type="admin", is_admin=True)
    resp = await create_test_participant(participant_body=is_admin_true_body)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_random_participant_missing_required_fields(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    missing_req_fields_body = generate_participant_request_body(registration_type="admin", name=None)
    resp = await create_test_participant(participant_body=missing_req_fields_body)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["type"] == "missing"
    assert resp_json["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_admin_participant(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    resp = await create_test_participant(participant_body=admin_participant_body)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == TEST_USER_NAME
    assert resp_json["participant"]["email"] == TEST_USER_EMAIL
    assert resp_json["participant"]["is_admin"] is True
    assert resp_json["participant"]["email_verified"] is False
    assert resp_json["participant"]["team_id"] == resp_json["team"]["id"]
    assert resp_json["team"]["name"] == TEST_TEAM_NAME
    assert resp_json["team"]["is_verified"] is False


# The following test shows the order of create operations when adding an admin participant:
# We first create the team --> create the admin
# That is why when trying to create the same admin we get the message that the team already exists.
# We tried to create a team with the same name twice and the app throws an exception in that moment.
@pytest.mark.asyncio
async def test_create_admin_participant_email_and_team_already_exists(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=admin_participant_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_team_already_exists(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    existing_team_name_body = generate_participant_request_body(
        registration_type="admin", email="testtest1@test.com", is_admin=True, team_name=TEST_TEAM_NAME
    )

    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=existing_team_name_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_email_already_exists(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    existing_team_name_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam1"
    )

    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=existing_team_name_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_participant_success(
    generate_participant_request_body: ParticipantRequestBodyCallable, async_client: AsyncClient
) -> None:

    result_1 = await async_client.post(
        PARTICIPANT_ENDPOINT_URL, json=generate_participant_request_body(registration_type="random", is_admin=None)
    )
    result_2 = await async_client.delete(
        url=f"{PARTICIPANT_ENDPOINT_URL}/{result_1.json()["participant"]["id"]}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert result_2.status_code == 200

    result_2_json = result_2.json()

    assert result_2_json["participant"]["name"] == TEST_USER_NAME
    assert result_2_json["participant"]["email"] == TEST_USER_EMAIL
    assert result_2_json["participant"]["is_admin"] is False
    assert result_2_json["participant"]["email_verified"] is False
    assert result_2_json["participant"]["team_id"] is None


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_participant_unauthorized(async_client: AsyncClient, mock_obj_id: str) -> None:

    result = await async_client.delete(
        url=f"{PARTICIPANT_ENDPOINT_URL}/{mock_obj_id}", headers={"Authorization": "Bearer FakeToken"}
    )

    assert result.status_code == 401
    assert result.json()["detail"] == "Unauthorized"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_participant_wrong_obj_id_format(async_client: AsyncClient) -> None:

    result = await async_client.delete(
        url=f"{PARTICIPANT_ENDPOINT_URL}/1", headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"}
    )

    assert result.status_code == 400
    assert result.json()["detail"] == "Wrong Object ID format"


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
@pytest.mark.asyncio
async def test_delete_participant_obj_id_doesnt_exist(async_client: AsyncClient, mock_obj_id: str) -> None:

    result = await async_client.delete(
        url=f"{PARTICIPANT_ENDPOINT_URL}/{mock_obj_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    assert result.status_code == 404
    assert result.json()["error"] == "The specified participant was not found"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_create_link_participant_succesful(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:
    admin_partcipant_body = generate_participant_request_body(
        registration_type="admin", email="testadmin@test.com", is_admin=True, team_name=TEST_TEAM_NAME
    )
    admin_resp = await create_test_participant(participant_body=admin_partcipant_body)
    assert admin_resp.status_code == 201

    admin_resp_json = admin_resp.json()["participant"]

    link_participant_body = generate_participant_request_body(registration_type="invite_link", team_name=TEST_TEAM_NAME)
    jwt_payload = JwtUserRegistration(
        sub=admin_resp_json["id"],
        team_id=admin_resp_json["team_id"],
        exp=sufficient_expiration_time,
    )
    encoded_token = JwtUtility.encode_data(data=jwt_payload)

    resp = await create_test_participant(participant_body=link_participant_body, jwt_token=encoded_token)
    assert resp.status_code == 201

    resp_json = resp.json()["participant"]
    assert resp_json["email"] == TEST_USER_EMAIL
    assert resp_json["email_verified"] == True
    assert resp_json["team_id"] == admin_resp_json["team_id"]


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_create_link_participant_team_capacity_exceeded(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:
    admin_partcipant_body = generate_participant_request_body(
        registration_type="admin", email="testadmin@test.com", is_admin=True, team_name=TEST_TEAM_NAME
    )
    admin_resp = await create_test_participant(participant_body=admin_partcipant_body)
    assert admin_resp.status_code == 201

    admin_resp_json = admin_resp.json()["participant"]
    jwt_payload = JwtUserRegistration(
        sub=admin_resp_json["id"],
        team_id=admin_resp_json["team_id"],
        exp=sufficient_expiration_time,
    )
    encoded_token = JwtUtility.encode_data(data=jwt_payload)

    for num in range(1, TeamsRepository.MAX_NUMBER_OF_TEAM_MEMBERS):
        link_participant_body = generate_participant_request_body(
            registration_type="invite_link", email=f"testtest{num}@gmail.com", team_name=TEST_TEAM_NAME
        )
        resp = await create_test_participant(participant_body=link_participant_body, jwt_token=encoded_token)
        assert resp.status_code == 201

    link_participant_body = generate_participant_request_body(
        registration_type="invite_link",
        email=f"testtest{TeamsRepository.MAX_NUMBER_OF_TEAM_MEMBERS}@gmail.com",
        team_name=TEST_TEAM_NAME,
    )
    resp = await create_test_participant(participant_body=link_participant_body, jwt_token=encoded_token)
    assert resp.status_code == 409

    resp_json = resp.json()
    assert resp_json["error"] == "Max team capacity has been reached"


@pytest.mark.asyncio
async def test_create_link_participant_jwt_token_missing(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:
    link_participant_body = generate_participant_request_body(registration_type="invite_link", team_name=TEST_TEAM_NAME)
    resp = await create_test_participant(participant_body=link_participant_body)
    assert resp.status_code == 409

    resp_json = resp.json()
    assert resp_json["error"] == "When `type` is 'invite_link' jwt_token is expected as a query param."


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_create_link_participant_jwt_wrong_format(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:
    link_participant_body = generate_participant_request_body(registration_type="invite_link", team_name=TEST_TEAM_NAME)
    resp = await create_test_participant(participant_body=link_participant_body, jwt_token="sldkf")
    assert resp.status_code == 400

    resp_json = resp.json()
    assert resp_json["error"] == "There was a a general error while decoding the JWT token. Checks its format again."


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_create_link_participant_team_name_mismatch(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
) -> None:
    admin_partcipant_body = generate_participant_request_body(
        registration_type="admin", email="testadmin@test.com", is_admin=True, team_name=TEST_TEAM_NAME
    )
    admin_resp = await create_test_participant(participant_body=admin_partcipant_body)
    assert admin_resp.status_code == 201

    admin_resp_json = admin_resp.json()["participant"]

    link_participant_body = generate_participant_request_body(registration_type="invite_link", team_name="testteam1")
    jwt_payload = JwtUserRegistration(
        sub=admin_resp_json["id"],
        team_id=admin_resp_json["team_id"],
        exp=sufficient_expiration_time,
    )
    encoded_token = JwtUtility.encode_data(data=jwt_payload)

    resp = await create_test_participant(participant_body=link_participant_body, jwt_token=encoded_token)
    assert resp.status_code == 400

    resp_json = resp.json()
    assert (
        resp_json["error"]
        == "team_name passed in the request body is different from the team_name in the decoded JWT token"
    )
