from datetime import timedelta, datetime
from typing import cast

from unittest.mock import Mock, patch

from bson import ObjectId
import pytest
from result import Ok, Err

from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    EmailRateLimitExceededError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNameMissmatchError,
    TeamNotFoundError,
)
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
)
from src.service.hackathon.admin_team_service import AdminTeamService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.team_service import TeamService
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_NAME
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    FeatureSwitchRepoMock,
    HackathonMailServiceMock,
    BackgroundTasksMock,
    MongoTransactionManagerMock,
    TeamServiceMock,
    ParticipantServiceMock,
)
from src.service.constants import MAX_NUMBER_OF_TEAM_MEMBERS

PARTICIPANT_LAST_SENT_EMAIL_VALID_RANGE = datetime.now() - timedelta(seconds=180)
PARTICIPANT_LAST_SENT_EMAIL_INVALID_RANGE = datetime.now() - timedelta(seconds=30)


@pytest.fixture
def hackathon_utility_service(
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    team_service_mock: TeamServiceMock,
    feature_switch_repo_mock: FeatureSwitchRepoMock,
) -> HackathonUtilityService:
    return HackathonUtilityService(
        cast(ParticipantsRepository, participant_repo_mock),
        cast(TeamsRepository, team_repo_mock),
        cast(TeamService, team_service_mock),
        cast(FeatureSwitchRepository, feature_switch_repo_mock),
    )


@pytest.fixture
def team_service(
    participant_repo_mock: ParticipantRepoMock,
    participant_service_mock: ParticipantServiceMock,
    team_repo_mock: TeamRepoMock,
    team_service_mock: TeamServiceMock,
    tx_manager_mock: MongoTransactionManagerMock,
) -> TeamService:
    return TeamService(
        cast(TeamsRepository, team_repo_mock),
        cast(ParticipantService, participant_service_mock),
        cast(ParticipantsRepository, participant_repo_mock),
        cast(MongoTransactionManager, tx_manager_mock),
    )


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


@pytest.fixture
def admin_team_service(
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
) -> AdminTeamService:
    return AdminTeamService(
        cast(TeamsRepository, team_repo_mock),
        cast(ParticipantsRepository, participant_repo_mock),
        cast(MongoTransactionManager, tx_manager_mock),
    )


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction(
    admin_team_service: AdminTeamService,
    admin_case_input_data_mock: AdminParticipantInputData,
    participant_repo_mock: ParticipantRepoMock,
    admin_participant_mock: Participant,
    unverified_team_mock: Team,
    team_repo_mock: TeamRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
) -> None:
    # Given
    # Mock successful `create` responses for team and participant
    team_repo_mock.create.return_value = unverified_team_mock
    participant_repo_mock.create.return_value = admin_participant_mock
    # Mock successful transaction result
    tx_manager_mock.with_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # When
    result = await admin_team_service.create_participant_and_team_in_transaction(admin_case_input_data_mock)

    # Then
    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_duplicate_team_name_err(
    admin_team_service: AdminTeamService,
    admin_case_input_data_mock: AdminParticipantInputData,
    tx_manager_mock: MongoTransactionManagerMock,
) -> None:
    # Given
    # Mock an `Err` for duplicate team name returned from transaction
    tx_manager_mock.with_transaction.return_value = Err(DuplicateTeamNameError(admin_case_input_data_mock.team_name))

    # When
    result = await admin_team_service.create_participant_and_team_in_transaction(admin_case_input_data_mock)

    # Then
    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == admin_case_input_data_mock.team_name


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_duplicate_email_err(
    admin_team_service: AdminTeamService,
    admin_case_input_data_mock: AdminParticipantInputData,
    tx_manager_mock: MongoTransactionManagerMock,
) -> None:
    # Given
    # Mock an `Err` for duplicate email returned from transaction
    tx_manager_mock.with_transaction.return_value = Err(DuplicateEmailError(admin_case_input_data_mock.email))

    # When
    result = await admin_team_service.create_participant_and_team_in_transaction(admin_case_input_data_mock)

    # Then
    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == admin_case_input_data_mock.email


@pytest.mark.asyncio
async def test_register_admin_participant_general_exception(
    admin_team_service: AdminTeamService,
    admin_case_input_data_mock: AdminParticipantInputData,
    tx_manager_mock: MongoTransactionManagerMock,
) -> None:
    # Given
    # Mock `with_transaction` to raise a general exception
    tx_manager_mock.with_transaction.return_value = Err(Exception("Test error"))

    # When
    result = await admin_team_service.create_participant_and_team_in_transaction(admin_case_input_data_mock)

    # Then
    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_sufficient_capacity(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 18
    team_repo_mock.get_verified_registered_teams_count.return_value = 4

    # When
    # Call the admin case capacity check function
    result = await hackathon_utility_service.check_capacity_register_admin_participant_case()

    # Then
    # Assert the result is True (enough capacity)
    assert result is True


@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_exact_limit(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 10
    team_repo_mock.get_verified_registered_teams_count.return_value = 14

    # When
    # Call the admin case capacity check function
    result = await hackathon_utility_service.check_capacity_register_admin_participant_case()

    # Then
    # Assert the result is False (capacity exactly reached)
    assert result is False


@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_exceeded_capacity(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 20
    team_repo_mock.get_verified_registered_teams_count.return_value = 14

    # When
    # Call the admin case capacity check function
    result = await hackathon_utility_service.check_capacity_register_admin_participant_case()

    # Then
    # Assert the result is False (capacity exceeded)
    assert result is False


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
async def test_check_capacity_random_case_with_sufficient_capacity(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 18
    team_repo_mock.get_verified_registered_teams_count.return_value = 4

    # When
    # Call the random case capacity check function
    result = await hackathon_utility_service.check_capacity_register_random_participant_case()

    # Then
    # Assert the result is True (enough capacity)
    assert result is True


@pytest.mark.asyncio
async def test_check_capacity_random_case_with_exact_limit(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 10
    team_repo_mock.get_verified_registered_teams_count.return_value = 10

    # When
    # Call the random case capacity check function
    result = await hackathon_utility_service.check_capacity_register_random_participant_case()

    # Then
    # Assert the result is True (capacity exactly reached)
    assert result is True


@pytest.mark.asyncio
async def test_check_capacity_random_case_with_exceeded_capacity(
    hackathon_utility_service: HackathonUtilityService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
) -> None:
    # Given
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 20
    team_repo_mock.get_verified_registered_teams_count.return_value = 14

    # When
    # Call the admin case capacity check function
    result = await hackathon_utility_service.check_capacity_register_random_participant_case()

    # Then
    # Assert the result is False (capacity exceeded)
    assert result is False


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_success(
    admin_team_service: AdminTeamService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    mock_verified_team: Team,
    mock_admin_participant: Participant,
    tx_manager_mock: MongoTransactionManagerMock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:
    # Given
    mock_admin_participant.email_verified = True
    mock_verified_admin_participant = mock_admin_participant
    # Mocks update for team and participants repo
    team_repo_mock.update.return_value = mock_verified_team
    participant_repo_mock.update.return_value = mock_verified_admin_participant

    # Result the callback passed to with_transaction
    tx_manager_mock.with_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # When
    result = await admin_team_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    # Then
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)
    assert result.ok_value[0].email_verified == True
    assert result.ok_value[1].is_verified == True


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_team_not_found_error(
    admin_team_service: AdminTeamService,
    tx_manager_mock: MongoTransactionManagerMock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:
    # Given
    tx_manager_mock.with_transaction.return_value = Err(TeamNotFoundError())

    # When
    result = await admin_team_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_general_error(
    admin_team_service: AdminTeamService,
    tx_manager_mock: MongoTransactionManagerMock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:
    # Given
    tx_manager_mock.with_transaction.return_value = Err(Exception("Test error"))

    # When
    result = await admin_team_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    # Then
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    str(result.err_value) == "Test error"


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
async def test_check_team_capacity_case_available_space(
    team_service: TeamService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    obj_id_mock: str,
) -> None:
    # Given
    # Mock the get_number_registered_teammates() to return a number that is less that the MAX_NUMBER_OF_TEAM_MEMEBERS
    participant_repo_mock.get_number_registered_teammates.return_value = MAX_NUMBER_OF_TEAM_MEMBERS - 1

    # When
    result = await team_service.check_team_capacity(obj_id_mock)

    # Then
    assert result is True


@pytest.mark.asyncio
async def test_check_team_capacity_case_capacity_exceeded(
    team_service: TeamService,
    participant_repo_mock: ParticipantRepoMock,
    team_repo_mock: TeamRepoMock,
    obj_id_mock: str,
) -> None:
    # Given
    participant_repo_mock.get_number_registered_teammates.return_value = MAX_NUMBER_OF_TEAM_MEMBERS

    # When
    result = await team_service.check_team_capacity(obj_id_mock)

    # Then
    assert result is False


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
