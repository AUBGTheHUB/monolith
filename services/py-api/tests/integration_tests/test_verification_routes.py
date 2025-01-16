from unittest.mock import patch
from httpx import AsyncClient
import pytest
from src.database.repository.teams_repository import TeamsRepository
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerificationData
from src.utils import JwtUtility
from tests.integration_tests.conftest import CreateTestParticipantCallable, ParticipantRequestBodyCallable
from tests.integration_tests.conftest import PARTICIPANT_VERIFY_URL
from starlette import status


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_success(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
    async_client: AsyncClient,
    thirty_sec_jwt_exp_limit: float,
) -> None:
    # Generate random participant body
    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    # Create random participant
    create_resp = await create_test_participant(participant_body=random_participant_body)
    # Assert that the participant was created successfully
    assert create_resp.status_code == status.HTTP_201_CREATED

    create_resp_json = create_resp.json()

    # Generate jwt token based on the random participant that was created
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=create_resp_json["participant"]["id"], is_admin=False, exp=thirty_sec_jwt_exp_limit
    )
    verify_jwt_token = JwtUtility.encode_data(data=verify_jwt_token_payload)

    # Make call to the endpoint to verify participant
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")

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


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_not_found(
    async_client: AsyncClient, mock_obj_id: str, thirty_sec_jwt_exp_limit: float
) -> None:
    # Generate jwt token based on a mock object id that does not exist on the database
    verify_jwt_token_payload = JwtParticipantVerificationData(
        sub=mock_obj_id, is_admin=False, exp=thirty_sec_jwt_exp_limit
    )
    verify_jwt_token = JwtUtility.encode_data(data=verify_jwt_token_payload)

    # Make call to the endpoint to verify participant
    verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")

    # Assert that the verification was not successful. The participant that we are trying to verify is missing
    assert verify_resp.status_code == status.HTTP_404_NOT_FOUND

    verify_resp_json = verify_resp.json()
    # Check the error message
    assert verify_resp_json["error"] == "The specified participant was not found"


@patch.object(TeamsRepository, "MAX_NUMBER_OF_TEAM_MEMBERS", 2)
@patch.object(TeamsRepository, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 1)
@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_hackathon_capacity_exceeded(
    create_test_participant: CreateTestParticipantCallable,
    generate_participant_request_body: ParticipantRequestBodyCallable,
    async_client: AsyncClient,
    thirty_sec_jwt_exp_limit: float,
) -> None:
    # Buffer for the created unverified participants
    created_participant_ids = []

    # Create 3 unverified random participants - Shows that you can create more unverified random participants than the max cap.
    for i in range(TeamsRepository.MAX_NUMBER_OF_TEAM_MEMBERS + 1):
        # Generate random participant body
        random_participant_body = generate_participant_request_body(
            registration_type="random", email=f"test{i}@test.com", is_admin=None
        )
        # Create random participant
        create_resp = await create_test_participant(participant_body=random_participant_body)
        assert create_resp.status_code == status.HTTP_201_CREATED

        create_resp_json = create_resp.json()
        created_participant_ids.append(create_resp_json["participant"]["id"])

    # We try to verify each of them, but we should only be able to verify up to the capacity
    for i in range(TeamsRepository.MAX_NUMBER_OF_TEAM_MEMBERS + 1):
        # Generate jwt token based on a mock object id that does not exist on the database
        verify_jwt_token_payload = JwtParticipantVerificationData(
            sub=created_participant_ids.pop(), is_admin=False, exp=thirty_sec_jwt_exp_limit
        )
        verify_jwt_token = JwtUtility.encode_data(data=verify_jwt_token_payload)
        # Make call to the endpoint to verify participant
        verify_resp = await async_client.patch(url=f"{PARTICIPANT_VERIFY_URL}?jwt_token={verify_jwt_token}")
        verify_resp_json = verify_resp.json()

        # Make assertions conditionally
        # Verification is successful only up to capacity
        if i < TeamsRepository.MAX_NUMBER_OF_TEAM_MEMBERS:
            assert verify_resp.status_code == status.HTTP_200_OK
        else:
            assert verify_resp.status_code == status.HTTP_409_CONFLICT
            assert verify_resp_json["error"] == "Max hackathon capacity has been reached"
