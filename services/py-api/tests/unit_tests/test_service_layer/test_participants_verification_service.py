from typing import cast

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
from src.service.hackathon.admin_team_service import AdminTeamService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.verification_service import VerificationService
from src.service.hackathon.team_service import TeamService
from src.service.jwt_utils.schemas import JwtParticipantVerificationData
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import (
    HackathonServiceMock,
    TeamRepoMock,
    BackgroundTasksMock,
    ParticipantRepoMock,
    TeamServiceMock,
    ParticipantServiceMock,
    AdminTeamServiceMock,
    HackathonMailServiceMock,
)


@pytest.fixture
def p_ver_service(
    hackathon_utility_service_mock: HackathonServiceMock,
    team_service_mock: TeamServiceMock,
    participant_service_mock: ParticipantServiceMock,
    admin_team_service_mock: AdminTeamServiceMock,
    hackathon_mail_service_mock: HackathonMailServiceMock,
) -> VerificationService:
    return VerificationService(
        cast(HackathonUtilityService, hackathon_utility_service_mock),
        cast(TeamService, team_service_mock),
        cast(ParticipantService, participant_service_mock),
        cast(AdminTeamService, admin_team_service_mock),
        cast(HackathonMailService, hackathon_mail_service_mock),
    )


@pytest.mark.asyncio
async def test_verify_admin_participant_success(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    verified_team_mock: Team,
    verified_admin_participant_mock: Participant,
    participant_repo_mock: ParticipantRepoMock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    hackathon_utility_service_mock.send_successful_registration_email = Mock(return_value=None)
    # Mock update methods for team and participants repos
    team_repo_mock.update.return_value = verified_team_mock
    participant_repo_mock.update.return_value = verified_admin_participant_mock
    hackathon_utility_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.update.return_value, team_repo_mock.update.return_value)
    )

    # When
    result = await p_ver_service.verify_admin_participant(
        jwt_admin_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
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
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    hackathon_utility_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(
        ParticipantNotFoundError()
    )

    # When
    result = await p_ver_service.verify_admin_participant(
        jwt_admin_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_verify_admin_participant_team_not_found_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    hackathon_utility_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(
        TeamNotFoundError()
    )

    # When
    result = await p_ver_service.verify_admin_participant(
        jwt_admin_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def test_verify_admin_participant_general_exeption(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    hackathon_utility_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Err(Exception())

    # When
    result = await p_ver_service.verify_admin_participant(
        jwt_admin_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_verify_admin_participant_hackathon_capacity_exceeded_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    verified_team_mock: Team,
    verified_admin_participant_mock: Participant,
    participant_repo_mock: ParticipantRepoMock,
    jwt_admin_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = False
    # Mock update methods for team and participants repos
    team_repo_mock.update.return_value = verified_team_mock
    participant_repo_mock.update.return_value = verified_admin_participant_mock
    hackathon_utility_service_mock.verify_admin_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.update.return_value, team_repo_mock.update.return_value)
    )

    # When
    result = await p_ver_service.verify_admin_participant(
        jwt_admin_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_verify_random_participant_success(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_repo_mock: ParticipantRepoMock,
    verified_random_participant_mock: Participant,
    background_tasks_mock: BackgroundTasksMock,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    hackathon_utility_service_mock.send_successful_registration_email = Mock(return_value=None)
    participant_repo_mock.update.return_value = verified_random_participant_mock
    hackathon_utility_service_mock.verify_random_participant.return_value = Ok(
        (participant_repo_mock.update.return_value, None)
    )

    # When
    result = await p_ver_service.verify_random_participant(
        jwt_random_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert result.ok_value[1] is None
    assert result.ok_value[0].name == TEST_USER_NAME
    assert result.ok_value[0].email_verified == True


@pytest.mark.asyncio
async def test_verify_random_participant_participant_not_found_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    hackathon_utility_service_mock.verify_random_participant.return_value = Err(ParticipantNotFoundError())

    # When
    result = await p_ver_service.verify_random_participant(
        jwt_random_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_verify_random_participant_general_exception(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    hackathon_utility_service_mock.verify_random_participant.return_value = Err(Exception())

    # When
    result = await p_ver_service.verify_random_participant(
        jwt_random_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)


@pytest.mark.asyncio
async def test_verify_random_participant_hackathon_capacity_exceeded_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    verified_random_participant_mock: Participant,
    jwt_random_user_verification_mock: JwtParticipantVerificationData,
) -> None:
    # Given
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = False
    participant_repo_mock.update.return_value = verified_random_participant_mock
    hackathon_utility_service_mock.verify_random_participant.return_value = Ok(
        (participant_repo_mock.update.return_value, None)
    )

    # When
    result = await p_ver_service.verify_random_participant(
        jwt_random_user_verification_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_send_verification_email_success(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    admin_participant_mock: Participant,
    unverified_team_mock: Team,
    background_tasks_mock: BackgroundTasksMock,
    obj_id_mock: str,
) -> None:
    # Given
    participant_mock_value = admin_participant_mock
    team_mock_value = unverified_team_mock
    hackathon_utility_service_mock.check_send_verification_email_rate_limit.return_value = Ok(
        (participant_mock_value, team_mock_value)
    )
    # Mock no err when sending verification email
    hackathon_utility_service_mock.send_verification_email = AsyncMock(return_value=None)

    # When
    result = await p_ver_service.resend_verification_email(obj_id_mock, cast(BackgroundTasks, background_tasks_mock))

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, Participant)
    assert result.ok_value.name == TEST_USER_NAME
    assert result.ok_value.email == TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_send_verification_email_rate_limit_exceeded_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    obj_id_mock: str,
) -> None:
    # Given
    hackathon_utility_service_mock.check_send_verification_email_rate_limit.return_value = Err(
        EmailRateLimitExceededError(seconds_to_retry_after=30)
    )

    # When
    result = await p_ver_service.resend_verification_email(obj_id_mock, cast(BackgroundTasks, background_tasks_mock))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, EmailRateLimitExceededError)


@pytest.mark.asyncio
async def test_send_verification_email_participant_not_found_error(
    p_ver_service: VerificationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    obj_id_mock: str,
) -> None:
    # Given
    hackathon_utility_service_mock.check_send_verification_email_rate_limit.return_value = Err(
        ParticipantNotFoundError()
    )

    # When
    result = await p_ver_service.resend_verification_email(obj_id_mock, cast(BackgroundTasks, background_tasks_mock))

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)
