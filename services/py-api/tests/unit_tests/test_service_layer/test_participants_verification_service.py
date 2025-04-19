from fastapi import BackgroundTasks
import pytest

from result import Err, Ok
from unittest.mock import Mock, AsyncMock

from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import (
    EmailRateLimitExceededError,
    HackathonCapacityExceededError,
    ParticipantNotFoundError,
    TeamNotFoundError,
)
from src.service.hackathon.participants_verification_service import ParticipantVerificationService
from src.service.jwt_utils.schemas import JwtParticipantVerificationData
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME


@pytest.fixture
def p_ver_service(hackathon_service_mock: Mock) -> ParticipantVerificationService:
    return ParticipantVerificationService(hackathon_service_mock)


@pytest.mark.asyncio
async def test_verify_admin_participant_success(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: BackgroundTasks,
    verified_team_mock: Team,
    verified_admin_participant_mock: Participant,
    participant_repo_mock: Mock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True
    hackathon_service_mock.send_successful_registration_email = Mock(return_value=None)

    # Mock update methods for team and participants repos
    team_repo_mock.update.return_value = verified_team_mock
    participant_repo_mock.update.return_value = verified_admin_participant_mock

    hackathon_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.update.return_value, team_repo_mock.update.return_value)
    )

    result = await p_ver_service.verify_admin_participant(jwt_admin_user_verification_mock, background_tasks)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)
    assert result.ok_value[0].name == TEST_USER_NAME
    assert result.ok_value[1].name == TEST_TEAM_NAME
    assert result.ok_value[0].email_verified == True
    assert result.ok_value[1].is_verified == True


@pytest.mark.asyncio
async def test_verify_admin_participant_participant_not_found_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    hackathon_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(
        ParticipantNotFoundError()
    )

    result = await p_ver_service.verify_admin_participant(jwt_admin_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_verify_admin_participant_team_not_found_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    hackathon_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(TeamNotFoundError())

    result = await p_ver_service.verify_admin_participant(jwt_admin_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_verify_admin_participant_general_exeption(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    hackathon_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(
        Exception("Test exception")
    )

    result = await p_ver_service.verify_admin_participant(jwt_admin_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    str(result.err_value) == "Test exception"


@pytest.mark.asyncio
async def test_verify_admin_participant_hackathon_capacity_exceeded_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: BackgroundTasks,
    verified_team_mock: Team,
    verified_admin_participant_mock: Participant,
    participant_repo_mock: Mock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = False

    # Mock update methods for team and participants repos
    team_repo_mock.update.return_value = verified_team_mock
    participant_repo_mock.update.return_value = verified_admin_participant_mock

    hackathon_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.update.return_value, team_repo_mock.update.return_value)
    )

    result = await p_ver_service.verify_admin_participant(jwt_admin_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_verify_random_participant_success(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    participant_repo_mock: Mock,
    verified_random_participant_mock: Participant,
    background_tasks: BackgroundTasks,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True
    hackathon_service_mock.send_successful_registration_email = Mock(return_value=None)

    participant_repo_mock.update.return_value = verified_random_participant_mock

    hackathon_service_mock.verify_random_participant.return_value = Ok(
        (participant_repo_mock.update.return_value, None)
    )

    result = await p_ver_service.verify_random_participant(jwt_random_user_verification_mock, background_tasks)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert result.ok_value[1] is None
    assert result.ok_value[0].name == TEST_USER_NAME
    assert result.ok_value[0].email_verified == True


@pytest.mark.asyncio
async def test_verify_random_participant_participant_not_found_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True

    hackathon_service_mock.verify_random_participant.return_value = Err(ParticipantNotFoundError())

    result = await p_ver_service.verify_random_participant(jwt_random_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_verify_random_participant_general_exception(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True

    hackathon_service_mock.verify_random_participant.return_value = Err(Exception())

    result = await p_ver_service.verify_random_participant(jwt_random_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_verify_random_participant_hackathon_capacity_exceeded_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    participant_repo_mock: Mock,
    background_tasks: BackgroundTasks,
    verified_random_participant_mock: Participant,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = False

    participant_repo_mock.update.return_value = verified_random_participant_mock

    hackathon_service_mock.verify_random_participant.return_value = Ok(
        (participant_repo_mock.update.return_value, None)
    )

    result = await p_ver_service.verify_random_participant(jwt_random_user_verification_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_send_verification_email_success(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    admin_participant_mock: Participant,
    unverified_team_mock: Team,
    background_tasks: BackgroundTasks,
    obj_id_mock: str,
) -> None:
    participant_mock_value = admin_participant_mock

    team_mock_value = unverified_team_mock

    hackathon_service_mock.check_send_verification_email_rate_limit.return_value = Ok(
        (participant_mock_value, team_mock_value)
    )
    # Mock no err when sending verification email
    hackathon_service_mock.send_verification_email = AsyncMock(return_value=None)

    result = await p_ver_service.resend_verification_email(obj_id_mock, background_tasks)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_send_verification_email_rate_limit_exceeded_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    obj_id_mock: str,
) -> None:
    hackathon_service_mock.check_send_verification_email_rate_limit.return_value = Err(
        EmailRateLimitExceededError(seconds_to_retry_after=30)
    )

    result = await p_ver_service.resend_verification_email(obj_id_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, EmailRateLimitExceededError)


@pytest.mark.asyncio
async def test_send_verification_email_participant_not_found_error(
    p_ver_service: ParticipantVerificationService,
    hackathon_service_mock: Mock,
    background_tasks: BackgroundTasks,
    obj_id_mock: str,
) -> None:
    hackathon_service_mock.check_send_verification_email_rate_limit.return_value = Err(ParticipantNotFoundError())

    result = await p_ver_service.resend_verification_email(obj_id_mock, background_tasks)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)
