from unittest.mock import Mock, patch
from bson import ObjectId
import pytest
from result import Err, Ok
from src.database.model.participant_model import Participant
from src.server.exception import HackathonCapacityExceededError, ParticipantNotFoundError
from src.server.handlers.verification_handlers import VerificationHandlers
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserRegistration, JwtUserVerification
from src.server.schemas.response_schemas.schemas import ErrResponse, ParticipantVerifiedResponse, Response
from src.utils import JwtUtility
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME
from starlette import status


@pytest.fixture
def verification_handlers(participant_verification_service_mock: Mock) -> VerificationHandlers:
    return VerificationHandlers(participant_verification_service_mock)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_case_success(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    mock_jwt_random_user_verification: JwtUserVerification,
    mock_obj_id: str,
) -> None:
    # Mock successful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Ok(
        (
            Participant(
                id=mock_obj_id,
                name=TEST_USER_NAME,
                email=TEST_USER_EMAIL,
                is_admin=False,
                email_verified=True,
                team_id=ObjectId(),
            ),
            None,
        )
    )

    jwt_token = JwtUtility.encode_data(data=mock_jwt_random_user_verification)

    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token)

    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=mock_jwt_random_user_verification
    )

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantVerifiedResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is False
    assert resp.response_model.participant.email_verified is True
    assert resp.response_model.team is None
    assert resp.status_code == status.HTTP_200_OK


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_decode_error(
    verification_handlers: VerificationHandlers,
    mock_jwt_user_registration: JwtUserRegistration,
) -> None:
    # Create the token with the wrong schema
    jwt_token = JwtUtility.encode_data(data=mock_jwt_user_registration)

    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token)

    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The decoded token does not match the Jwt schema"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_not_found(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    mock_jwt_random_user_verification: JwtUserVerification,
) -> None:
    # Mock unsuccessful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Err(ParticipantNotFoundError())

    jwt_token = JwtUtility.encode_data(data=mock_jwt_random_user_verification)

    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token)

    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=mock_jwt_random_user_verification
    )

    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_hackathon_capacity_reached(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    mock_jwt_random_user_verification: JwtUserVerification,
) -> None:
    # Mock unsuccessful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Err(HackathonCapacityExceededError())

    jwt_token = JwtUtility.encode_data(data=mock_jwt_random_user_verification)

    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token)

    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=mock_jwt_random_user_verification
    )

    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"
