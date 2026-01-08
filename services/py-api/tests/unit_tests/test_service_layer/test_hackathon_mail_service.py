from unittest.mock import Mock, patch
from typing import cast
import pytest
from result import Ok, Err
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    HackathonMailServiceMock,
    BackgroundTasksMock,
)
from src.service.hackathon.participant_service import ParticipantService
from src.database.model.hackathon.participant_model import Participant
from src.exception import ParticipantNotFoundError
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.jwt_utils.codec import JwtUtility


@pytest.fixture
def participant_service(
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    jwt_utility_mock: JwtUtility,
    hackathon_mail_service_mock: HackathonMailServiceMock,
) -> ParticipantService:
    return ParticipantService(
        participants_repo=cast(ParticipantsRepository, participant_repo_mock),
        teams_repo=cast(TeamsRepository, team_repo_mock),
        hackathon_mail_service=cast(HackathonMailService, hackathon_mail_service_mock),
        jwt_utility=jwt_utility_mock,
    )


@pytest.mark.asyncio
async def test_send_verification_email_success(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    hackathon_mail_service_mock: Mock,
    admin_participant_mock: Participant,
) -> None:
    # Given
    hackathon_mail_service_mock.send_participant_verification_email.return_value = None
    # And no err from repo
    participant_repo_mock.update.return_value = Ok(admin_participant_mock)

    # As we don't send emails for testing env due to integration tests we have to patch this
    with patch("src.environment.ENV", return_value="DEV"):
        # When
        result = await participant_service.send_verification_email(
            participant=admin_participant_mock, background_tasks=background_tasks_mock
        )

        # Then
        assert isinstance(result, Ok)
        assert isinstance(result.ok_value, Participant)


@pytest.mark.asyncio
async def test_send_verification_email_err_validation_err_body_generation(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    hackathon_mail_service_mock: Mock,
    admin_participant_mock: Participant,
) -> None:
    # Given
    hackathon_mail_service_mock.send_participant_verification_email.return_value = Err(ValueError("Test Error"))
    # And no err from repo
    participant_repo_mock.update.return_value = Ok(admin_participant_mock)

    # As we don't send emails for testing env due to integration tests we have to patch this
    with patch("src.environment.ENV", return_value="DEV"):
        # When
        err = await participant_service.send_verification_email(
            participant=admin_participant_mock, background_tasks=background_tasks_mock
        )

        # Then
        # Assert err value returned while sending the email from hackathon service
        assert isinstance(err, Err)
        assert isinstance(err.err_value, ValueError)


@pytest.mark.asyncio
async def test_send_verification_email_err_participant_deleted_before_verifying_email(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    hackathon_mail_service_mock: Mock,
    admin_participant_mock: Participant,
) -> None:
    # Given
    hackathon_mail_service_mock.send_participant_verification_email.return_value = None
    participant_repo_mock.update.return_value = Err(ParticipantNotFoundError())

    # As we don't send emails for testing env due to integration tests we have to patch this
    with patch("src.environment.ENV", return_value="DEV"):
        # When
        err = await participant_service.send_verification_email(
            participant=admin_participant_mock, background_tasks=background_tasks_mock
        )

        # Then
        # Assert err value returned while sending the email from hackathon service
        assert isinstance(err, Err)
        assert isinstance(err.err_value, ParticipantNotFoundError)
