from typing import cast
from unittest.mock import Mock, patch
import pytest
from result import Err, Ok
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import (
    EmailRateLimitExceededError,
    HackathonCapacityExceededError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNotFoundError,
)
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantVerifiedResponse,
    Response,
    VerificationEmailSentSuccessfullyResponse,
)
from src.service.hackathon.participants_verification_service import ParticipantVerificationService
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from src.service.jwt_utils.codec import JwtUtility
from starlette import status
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import ParticipantVerificationServiceMock, BackgroundTasksMock


@pytest.fixture
def verification_handlers(
    participant_verification_service_mock: ParticipantVerificationServiceMock, jwt_utility_mock: JwtUtility
) -> VerificationHandlers:
    return VerificationHandlers(
        cast(ParticipantVerificationService, participant_verification_service_mock), jwt_utility_mock
    )


@pytest.mark.asyncio
async def test_verify_participant_admin_case_success(
    participant_verification_service_mock: Mock,
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    admin_participant_mock: Participant,
    jwt_utility_mock: JwtUtility,
    verified_team_mock: Team,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
    obj_id_mock: str,
) -> None:

    # Given
    admin_participant_mock.email_verified = True
    mock_verified_admin_participant = admin_participant_mock
    # Mock successful result from `verify_admin_participant`
    participant_verification_service_mock.verify_admin_participant.return_value = Ok(
        (
            mock_verified_admin_participant,
            verified_team_mock,
        )
    )

    # When
    jwt_token = jwt_utility_mock.encode_data(data=jwt_admin_user_verification_mock)
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)

    # Then
    participant_verification_service_mock.verify_admin_participant.assert_awaited_once()
    assert isinstance(resp, Response)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.response_model.participant.email_verified is True
    assert resp.response_model.team.is_verified is True


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_participant_admin_case_participant_not_found_error(
    participant_verification_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    verification_handlers: VerificationHandlers,
    jwt_utility_mock: JwtUtility,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    participant_verification_service_mock.verify_admin_participant.return_value = Err(ParticipantNotFoundError())
    jwt_token = jwt_utility_mock.encode_data(data=jwt_admin_user_verification_mock)

    # When
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)
    participant_verification_service_mock.verify_admin_participant.assert_awaited_once()

    # Then
    assert isinstance(resp, Response)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_participant_admin_case_team_not_found_error(
    participant_verification_service_mock: Mock,
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    participant_verification_service_mock.verify_admin_participant.return_value = Err(TeamNotFoundError())
    jwt_token = jwt_utility_mock.encode_data(data=jwt_admin_user_verification_mock)

    # When
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)
    participant_verification_service_mock.verify_admin_participant.assert_awaited_once()

    # Then
    assert isinstance(resp, Response)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"


@pytest.mark.asyncio
async def test_verify_participant_admin_case_hackation_capacity_reached_error(
    participant_verification_service_mock: Mock,
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    participant_verification_service_mock.verify_admin_participant.return_value = Err(HackathonCapacityExceededError())
    jwt_token = jwt_utility_mock.encode_data(data=jwt_admin_user_verification_mock)

    # When
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)
    participant_verification_service_mock.verify_admin_participant.assert_awaited_once()

    # Then
    assert isinstance(resp, Response)
    assert resp.status_code == status.HTTP_409_CONFLICT
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"


@pytest.mark.asyncio
async def test_verify_participant_admin_case_general_error(
    participant_verification_service_mock: Mock,
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    participant_verification_service_mock.verify_admin_participant.return_value = Err(Exception())
    jwt_token = jwt_utility_mock.encode_data(data=jwt_admin_user_verification_mock)

    # When
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)
    participant_verification_service_mock.verify_admin_participant.assert_awaited_once()

    # Then
    assert isinstance(resp, Response)
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"


@pytest.mark.asyncio
async def test_verify_random_participant_case_success(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    random_participant_mock: Participant,
    jwt_utility_mock: JwtUtility,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
    obj_id_mock: str,
) -> None:

    # Given
    random_participant_mock.email_verified = True
    mock_verified_random_participant = random_participant_mock
    # Mock successful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Ok(
        (
            mock_verified_random_participant,
            None,
        )
    )

    # When
    jwt_token = jwt_utility_mock.encode_data(data=jwt_random_user_verification_mock)
    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)

    # Then
    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=jwt_random_user_verification_mock, background_tasks=background_tasks_mock
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


@pytest.mark.asyncio
async def test_verify_random_participant_decode_error(
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_user_registration_mock: JwtParticipantInviteRegistrationData,
) -> None:

    # Given
    # Create the token with the wrong schema
    jwt_token = jwt_utility_mock.encode_data(data=jwt_user_registration_mock)

    # When
    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)

    # Then
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The decoded token does not match the Jwt schema"


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_verify_random_participant_not_found(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    # Mock unsuccessful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Err(ParticipantNotFoundError())

    # When
    jwt_token = jwt_utility_mock.encode_data(data=jwt_random_user_verification_mock)
    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)

    # Then
    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=jwt_random_user_verification_mock, background_tasks=background_tasks_mock
    )

    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"


@pytest.mark.asyncio
async def test_verify_random_hackathon_capacity_reached(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_utility_mock: JwtUtility,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:

    # Given
    # Mock unsuccessful result from `verify_random_participant`
    participant_verification_service_mock.verify_random_participant.return_value = Err(HackathonCapacityExceededError())

    jwt_token = jwt_utility_mock.encode_data(data=jwt_random_user_verification_mock)

    # When
    # Call the verification handler
    resp = await verification_handlers.verify_participant(jwt_token=jwt_token, background_tasks=background_tasks_mock)
    # Check that `verify_random_participant` was awaited once with the expected input_data
    participant_verification_service_mock.verify_random_participant.assert_awaited_once_with(
        jwt_data=jwt_random_user_verification_mock, background_tasks=background_tasks_mock
    )

    # Then
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"


@pytest.mark.asyncio
async def test_send_verification_email_success(
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    admin_participant_mock: Participant,
    jwt_utility_mock: JwtUtility,
    participant_verification_service_mock: Mock,
    obj_id_mock: str,
) -> None:

    # Given
    participant_verification_service_mock.resend_verification_email.return_value = Ok(admin_participant_mock)

    # When
    result = await verification_handlers.resend_verification_email(obj_id_mock, background_tasks_mock)

    # Then
    participant_verification_service_mock.resend_verification_email.assert_awaited_once()
    assert isinstance(result, Response)
    assert isinstance(result.response_model, VerificationEmailSentSuccessfullyResponse)
    assert result.status_code == status.HTTP_202_ACCEPTED
    assert result.response_model.participant.name == TEST_USER_NAME
    assert result.response_model.participant.email == TEST_USER_EMAIL
    assert result.response_model.participant.is_admin is True


@pytest.mark.asyncio
async def test_send_verification_email_rate_limit_exceeded_error(
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    admin_participant_mock: Participant,
    participant_verification_service_mock: Mock,
    obj_id_mock: str,
) -> None:

    # Given
    seconds_to_retry_after = 30
    participant_verification_service_mock.resend_verification_email.return_value = Err(
        EmailRateLimitExceededError(seconds_to_retry_after=seconds_to_retry_after)
    )

    # When
    result = await verification_handlers.resend_verification_email(obj_id_mock, background_tasks_mock)

    # Then
    participant_verification_service_mock.resend_verification_email.assert_awaited_once()
    assert isinstance(result, Response)
    assert isinstance(result.response_model, ErrResponse)
    assert result.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert result.response_model.error == (
        f"The rate limit for sending emails has been exceeded. Try again after " f"{seconds_to_retry_after} seconds."
    )


@pytest.mark.asyncio
async def test_send_verification_participant_alredy_verified_error(
    verification_handlers: VerificationHandlers,
    background_tasks_mock: BackgroundTasksMock,
    admin_participant_mock: Participant,
    participant_verification_service_mock: Mock,
    obj_id_mock: str,
) -> None:

    # Given
    participant_verification_service_mock.resend_verification_email.return_value = Err(
        ParticipantAlreadyVerifiedError()
    )

    # When
    result = await verification_handlers.resend_verification_email(obj_id_mock, background_tasks_mock)

    # Then
    participant_verification_service_mock.resend_verification_email.assert_awaited_once()
    assert isinstance(result, Response)
    assert isinstance(result.response_model, ErrResponse)
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.response_model.error == "You have already been verified"


@pytest.mark.asyncio
async def test_send_verification_participant_not_found_error(
    verification_handlers: VerificationHandlers,
    participant_verification_service_mock: Mock,
    jwt_utility_mock: JwtUtility,
    background_tasks_mock: BackgroundTasksMock,
    obj_id_mock: str,
) -> None:

    # Given
    participant_verification_service_mock.resend_verification_email.return_value = Err(ParticipantNotFoundError())

    # When
    result = await verification_handlers.resend_verification_email(obj_id_mock, background_tasks_mock)

    # Then
    participant_verification_service_mock.resend_verification_email.assert_awaited_once()
    assert isinstance(result, Response)
    assert isinstance(result.response_model, ErrResponse)
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert result.response_model.error == "The specified participant was not found"
