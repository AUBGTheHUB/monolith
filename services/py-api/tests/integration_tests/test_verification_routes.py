from datetime import datetime, timezone
from os import environ
from unittest.mock import patch
from httpx import AsyncClient
import pytest

from src.service.hackathon.constants import MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON, MAX_NUMBER_OF_TEAM_MEMBERS
from src.service.jwt_utils.schemas import JwtParticipantVerificationData
from src.service.jwt_utils.codec import JwtUtility
from tests.integration_tests.conftest import (
    TEST_TEAM_NAME,
    CreateTestParticipantCallable,
    ParticipantRequestBodyCallable,
    TEAM_ENDPOINT_URL,
)
from tests.integration_tests.conftest import PARTICIPANT_VERIFY_URL
from starlette import status


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_participant_admin_case_success(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    create_resp = await create_test_participant(participant_body=admin_participant_body)
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate jwt token based on the Object Id of the admin participant that we just created
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=create_resp_json["participant"]["id"], is_admin=True, exp=one_minute_jwt_exp
    )

    jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

    # When
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")

    # Then
    assert verify_resp.status_code == status.HTTP_200_OK

    verify_resp_json = verify_resp.json()
    assert create_resp_json["team"]["id"] == verify_resp_json["team"]["id"]
    assert create_resp_json["participant"]["id"] == verify_resp_json["participant"]["id"]
    assert create_resp_json["participant"]["team_id"] == create_resp_json["team"]["id"]
    assert verify_resp_json["participant"]["team_id"] == verify_resp_json["team"]["id"]
    assert create_resp_json["team"]["is_verified"] is False
    assert create_resp_json["participant"]["email_verified"] is False
    assert verify_resp_json["team"]["is_verified"] is True
    assert verify_resp_json["participant"]["email_verified"] is True


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_participant_admin_case_when_participant_is_not_found(
    obj_id_mock: str,
    one_minute_jwt_exp: int,
    jwt_utility_mock: JwtUtility,
    async_client: AsyncClient,
) -> None:
    # Given
    jwt_token = jwt_utility_mock.encode_data(
        data=JwtParticipantVerificationData(sub=obj_id_mock, is_admin=True, exp=one_minute_jwt_exp)
    )

    # When
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")

    # Then
    verify_resp_json = verify_resp.json()
    assert verify_resp.status_code == status.HTTP_404_NOT_FOUND
    assert verify_resp_json["error"] == "The specified participant was not found"


@patch.dict(
    "os.environ",
    {"SECRET_KEY": "abcdefghijklmnopqrst", "SECRET_AUTH_TOKEN": "OFFLINE_TOKEN", "RESEND_API_KEY": "res_some_api_key"},
)
@pytest.mark.asyncio
async def test_verify_participant_admin_case_when_team_is_not_found(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    create_resp = await create_test_participant(participant_body=admin_participant_body)
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    jwt_token = jwt_utility_mock.encode_data(
        data=JwtParticipantVerificationData(
            sub=create_resp_json["participant"]["id"], is_admin=True, exp=one_minute_jwt_exp
        )
    )

    delete_team_resp = await async_client.delete(
        url=f"{TEAM_ENDPOINT_URL}/{create_resp_json["team"]["id"]}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )
    assert delete_team_resp.status_code == status.HTTP_200_OK

    # When
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")

    # Then
    verify_resp_json = verify_resp.json()
    assert verify_resp.status_code == status.HTTP_404_NOT_FOUND
    assert verify_resp_json["error"] == "The specified team was not found"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_participant_admin_case_expired_token(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    jwt_utility_mock: JwtUtility,
    async_client: AsyncClient,
) -> None:
    # Given
    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    create_resp = await create_test_participant(participant_body=admin_participant_body)
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate an expired jwt token based on the Object Id of the admin participant that we just created
    jwt_token = jwt_utility_mock.encode_data(
        data=JwtParticipantVerificationData(
            sub=create_resp_json["participant"]["id"],
            is_admin=True,
            exp=int((datetime.now(tz=timezone.utc)).timestamp()),
        )
    )

    # When
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")

    # Then
    verfiy_resp_json = verify_resp.json()
    assert verify_resp.status_code == status.HTTP_400_BAD_REQUEST
    assert verfiy_resp_json["error"] == "The JWT token has expired."


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_admin_participant_hackathon_capacity_exceeded(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    # Buffer for the created unverified participants
    created_participant_ids = []

    # Create cap+1 unverified admin participants - Shows that you can create more unverified admin participants than the max cap.
    for i in range(MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON + 1):
        # Generate admin participant body
        admin_participant_body = generate_participant_request_body(
            registration_type="admin", email=f"test{i}@test.com", is_admin=True, team_name=f"{TEST_TEAM_NAME}{i}"
        )
        # Create admin participant
        create_resp = await create_test_participant(participant_body=admin_participant_body)
        assert create_resp.status_code == status.HTTP_201_CREATED

        create_resp_json = create_resp.json()
        created_participant_ids.append(create_resp_json["participant"]["id"])

    # When
    # We try to verify each of them, but we should only be able to verify up to the capacity
    for i in range(MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON + 1):
        # Generate jwt token based on a mock object id that does not exist on the database
        verify_jwt_token_payload = JwtParticipantVerificationData(
            sub=created_participant_ids.pop(), is_admin=True, exp=one_minute_jwt_exp
        )
        verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)
        # Make call to the endpoint to verify participant
        verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
        verify_resp_json = verify_resp.json()

        # Then
        # Make assertions conditionally
        # Verification is successful only up to capacity
        if i < MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON:
            assert verify_resp.status_code == status.HTTP_200_OK
            # TODO: Here a feature switch is flipped on the background - we should revert it somehow
        else:
            assert verify_resp.status_code == status.HTTP_409_CONFLICT
            assert verify_resp_json["error"] == "Max hackathon capacity has been reached"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_admin_participant_case_already_verified(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name=TEST_TEAM_NAME
    )
    create_resp = await create_test_participant(participant_body=admin_participant_body)
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate jwt token based on the Object Id of the admin participant that we just created
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=create_resp_json["participant"]["id"], is_admin=True, exp=one_minute_jwt_exp
    )

    jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

    # When
    # Try to verify the participant twice
    await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={jwt_token}")
    assert verify_resp.status_code == status.HTTP_400_BAD_REQUEST

    # Then
    # Check the error message
    verify_resp_json = verify_resp.json()
    assert verify_resp_json["error"] == "You have already been verified"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_random_participant_success(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    create_resp = await create_test_participant(participant_body=random_participant_body)
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate jwt token based on the random participant that was created
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=create_resp_json["participant"]["id"], is_admin=False, exp=one_minute_jwt_exp
    )
    verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

    # When
    # Make call to the endpoint to verify participant
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")

    # Then
    # Assert that the verification was successful
    assert verify_resp.status_code == status.HTTP_200_OK

    verify_resp_json = verify_resp.json()
    # Assert that this is the random participant that we created and the is_verify field is now true
    assert verify_resp_json["participant"]["id"] == create_resp_json["participant"]["id"]
    assert verify_resp_json["participant"]["name"] == create_resp_json["participant"]["name"]
    assert verify_resp_json["participant"]["email"] == create_resp_json["participant"]["email"]
    assert verify_resp_json["participant"]["is_admin"] == create_resp_json["participant"]["is_admin"]
    assert create_resp_json["participant"]["email_verified"] is False
    assert verify_resp_json["participant"]["email_verified"] is True
    assert create_resp_json["team"] is None
    assert verify_resp_json["team"] is None


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_random_participant_not_found(
    async_client: AsyncClient, obj_id_mock: str, jwt_utility_mock: JwtUtility, one_minute_jwt_exp: int
) -> None:
    # Given
    # Generate jwt token based on a mock object id that does not exist on the database
    verify_jwt_token_payload = JwtParticipantVerificationData(sub=obj_id_mock, is_admin=False, exp=one_minute_jwt_exp)
    verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

    # When
    # Make call to the endpoint to verify participant
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")

    # Then
    # Assert that the verification was not successful. The participant that we are trying to verify is missing
    assert verify_resp.status_code == status.HTTP_404_NOT_FOUND

    verify_resp_json = verify_resp.json()
    assert verify_resp_json["error"] == "The specified participant was not found"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_random_participant_hackathon_capacity_exceeded(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given

    # Create capacity-1 verified teams:
    for i in range(MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON - 1):
        # Generate admin participant body
        admin_participant_body = generate_participant_request_body(
            registration_type="admin", email=f"testadmin{i}@test.com", is_admin=True, team_name=f"{TEST_TEAM_NAME}{i}"
        )
        # Create admin participant
        create_resp = await create_test_participant(participant_body=admin_participant_body)
        assert create_resp.status_code == status.HTTP_201_CREATED

        verify_jwt_token_payload = JwtParticipantVerificationData(
            sub=create_resp.json()["participant"]["id"], is_admin=True, exp=one_minute_jwt_exp
        )
        verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

        # Make call to the endpoint to verify participant
        verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
        assert verify_resp.status_code == status.HTTP_200_OK

    # Buffer for the created unverified participants
    created_participant_ids = []

    # Create unverified random participants - Shows that you can create more unverified random participants than the max cap.
    for i in range(MAX_NUMBER_OF_TEAM_MEMBERS + 1):
        # Generate random participant body
        random_participant_body = generate_participant_request_body(
            registration_type="random", email=f"test{i}@test.com", is_admin=None
        )
        # Create random participant
        create_resp = await create_test_participant(participant_body=random_participant_body)
        assert create_resp.status_code == status.HTTP_201_CREATED

        create_resp_json = create_resp.json()
        created_participant_ids.append(create_resp_json["participant"]["id"])

    # When
    # We try to verify each of them, but we should only be able to verify up to the capacity
    for i in range(MAX_NUMBER_OF_TEAM_MEMBERS + 1):
        # Generate jwt token based on a mock object id that does not exist on the database
        verify_jwt_token_payload = JwtParticipantVerificationData(
            sub=created_participant_ids.pop(), is_admin=False, exp=one_minute_jwt_exp
        )
        verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)
        # Make call to the endpoint to verify participant
        verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
        verify_resp_json = verify_resp.json()

        # Then
        # Make assertions conditionally
        # Verification is successful only up to capacity
        if i < MAX_NUMBER_OF_TEAM_MEMBERS:
            assert verify_resp.status_code == status.HTTP_200_OK
        else:
            assert verify_resp.status_code == status.HTTP_409_CONFLICT
            assert verify_resp_json["error"] == "Max hackathon capacity has been reached"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst", "RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_verify_random_participant_case_already_verified(
    generate_participant_request_body: ParticipantRequestBodyCallable,
    create_test_participant: CreateTestParticipantCallable,
    async_client: AsyncClient,
    jwt_utility_mock: JwtUtility,
    one_minute_jwt_exp: int,
) -> None:
    # Given
    # Generate random participant body
    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    # Create random participant
    create_resp = await create_test_participant(participant_body=random_participant_body)
    # Assert that the participant was created successfully
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate jwt token based on the random participant that was created
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=create_resp_json["participant"]["id"], is_admin=False, exp=one_minute_jwt_exp
    )

    # When
    verify_jwt_token = jwt_utility_mock.encode_data(data=verify_jwt_token_payload)

    await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
    assert verify_resp.status_code == status.HTTP_400_BAD_REQUEST

    verify_resp_json = verify_resp.json()

    # Check the error message
    assert verify_resp_json["error"] == "You have already been verified"
