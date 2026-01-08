from typing import cast
from datetime import timedelta, datetime
import pytest
from bson import ObjectId
from result import Ok, Err
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    HackathonMailServiceMock,
    BackgroundTasksMock,
)
from src.service.jwt_utils.codec import JwtUtility
from src.service.hackathon.participant_service import ParticipantService
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.server.schemas.request_schemas.hackathon.schemas import (
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
)
from src.database.model.hackathon.participant_model import Participant
from src.exception import (
    DuplicateEmailError,
    EmailRateLimitExceededError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNameMissmatchError,
)
from unittest.mock import Mock, patch
from src.database.model.hackathon.team_model import Team
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_NAME


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
async def test_create_random_participant(
    participant_service: ParticipantService,
    random_case_input_data_mock: RandomParticipantInputData,
    random_participant_mock: Participant,
    participant_repo_mock: ParticipantRepoMock,
) -> None:
    # Given
    # Mock successful `create` response for random participant
    participant_repo_mock.create.return_value = Ok(random_participant_mock)

    # When
    result = await participant_service.create_random_participant(random_case_input_data_mock)

    # Then
    # Validate that the result is an `Ok` instance containing the participant object
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value[0], Participant)  # Check the first element is a Participant
    assert result.ok_value[0].name == random_case_input_data_mock.name
    assert result.ok_value[0].email == random_case_input_data_mock.email
    assert not result.ok_value[0].is_admin  # Ensure it is not an admin
    assert result.ok_value[1] is None  # Ensure the second element is None


@pytest.mark.asyncio
async def test_create_random_participant_duplicate_email_err(
    participant_service: ParticipantService,
    random_case_input_data_mock: RandomParticipantInputData,
    participant_repo_mock: ParticipantRepoMock,
) -> None:
    # Given
    # Mock the `create` method to simulate a duplicate email error
    duplicate_email_error = DuplicateEmailError(random_case_input_data_mock.email)
    participant_repo_mock.create.return_value = Err(duplicate_email_error)

    # When
    result = await participant_service.create_random_participant(random_case_input_data_mock)

    # Then
    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == random_case_input_data_mock.email


@pytest.mark.asyncio
async def test_create_random_participant_general_exception(
    participant_service: ParticipantService,
    random_case_input_data_mock: RandomParticipantInputData,
    participant_repo_mock: ParticipantRepoMock,
) -> None:
    # Given
    # Mock the `create` method to raise a general exception
    participant_repo_mock.create.return_value = Err(Exception("Test error"))

    # When
    result = await participant_service.create_random_participant(random_case_input_data_mock)

    # Then
    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_create_link_participant_duplicate_email_error(
    participant_service: ParticipantService,
    invite_link_case_input_data_mock: InviteLinkParticipantInputData,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    jwt_user_registration_mock: JwtParticipantInviteRegistrationData,
) -> None:
    # Given
    # Mock successful `fetch_by_id` response for link participant's team
    team_repo_mock.fetch_by_id.return_value = Ok(
        Team(id=ObjectId(jwt_user_registration_mock.team_id), name=invite_link_case_input_data_mock.team_name)
    )

    # Mock duplicate email error response for participant creation
    participant_repo_mock.create.return_value = Err(DuplicateEmailError(invite_link_case_input_data_mock.email))

    # When
    result = await participant_service.create_invite_link_participant(
        invite_link_case_input_data_mock, jwt_user_registration_mock
    )

    # Then
    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == invite_link_case_input_data_mock.email


@pytest.mark.asyncio
async def test_register_link_participant_team_name_mismatch(
    participant_service: ParticipantService,
    team_repo_mock: TeamRepoMock,
    invite_link_case_input_data_mock: InviteLinkParticipantInputData,
    jwt_user_registration_mock: JwtParticipantInviteRegistrationData,
) -> None:
    # Given
    # Modify the input_data to create a mismatch between the team names in the jwt and input data
    invite_link_case_input_data_mock.team_name = "modifiedteam"

    # Mock successful `fetch_by_id` response for link participant's team
    team_repo_mock.fetch_by_id.return_value = Ok(
        Team(id=ObjectId(jwt_user_registration_mock.team_id), name=TEST_TEAM_NAME)
    )

    # When
    # Call the function under test
    result = await participant_service.create_invite_link_participant(
        invite_link_case_input_data_mock, jwt_user_registration_mock
    )

    # Then
    # Check the err type
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNameMissmatchError)


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_success_random(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    team_repo_mock: TeamRepoMock,
    obj_id_mock: str,
) -> None:
    # Given
    participant_repo_mock.fetch_by_id.return_value = Ok(random_participant_mock)

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert result.ok_value[1] is None


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_not_reached_admin(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    admin_participant_mock: Participant,
    team_repo_mock: TeamRepoMock,
    obj_id_mock: str,
) -> None:
    # Given
    admin_participant_mock.last_sent_verification_email = datetime.now() - timedelta(seconds=180)
    participant_repo_mock.fetch_by_id.return_value = Ok(admin_participant_mock)
    team_repo_mock.fetch_by_id.return_value = Ok(Team(name=TEST_TEAM_NAME, is_verified=False))

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_limit_reached(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    obj_id_mock: str,
) -> None:
    # Given
    # Mock insufficient time delta for sending the emails
    random_participant_mock.last_sent_verification_email = datetime.now() - timedelta(seconds=30)
    participant_repo_mock.fetch_by_id.return_value = Ok(random_participant_mock)

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, EmailRateLimitExceededError)


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_without_last_sent_email(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    obj_id_mock: str,
) -> None:
    # Given
    # Mock participant who has not received a verification email yet
    random_participant_mock.last_sent_verification_email = None
    participant_repo_mock.fetch_by_id.return_value = Ok(random_participant_mock)

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert result.ok_value[1] is None
    assert result.ok_value[0].name == TEST_USER_NAME


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_already_verified(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    obj_id_mock: str,
) -> None:
    # Given
    random_participant_mock.email_verified = True
    participant_repo_mock.fetch_by_id.return_value = Ok(random_participant_mock)

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantAlreadyVerifiedError)


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_not_found(
    participant_service: ParticipantService,
    participant_repo_mock: ParticipantRepoMock,
    obj_id_mock: str,
) -> None:
    # Given
    participant_repo_mock.fetch_by_id.return_value = Err(ParticipantNotFoundError())

    # When
    result = await participant_service.check_send_verification_email_rate_limit(participant_id=obj_id_mock)

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


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
