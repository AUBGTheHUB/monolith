from datetime import timedelta, datetime

from unittest.mock import Mock, patch

from bson import ObjectId
import pytest
from result import Ok, Err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import (
    DuplicateTeamNameError,
    DuplicateEmailError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNameMissmatchError,
    TeamNotFoundError,
)
from src.server.schemas.jwt_schemas.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
)
from src.service.hackathon_service import HackathonService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME

PARTICIPANT_LAST_SENT_EMAIL_VALID_RANGE = datetime.now() - timedelta(seconds=180)
PARTICIPANT_LAST_SENT_EMAIL_INVALID_RANGE = datetime.now() - timedelta(seconds=30)


@pytest.fixture
def hackathon_service(participant_repo_mock: Mock, team_repo_mock: Mock, tx_manager_mock: Mock) -> HackathonService:
    return HackathonService(participant_repo_mock, team_repo_mock, tx_manager_mock)


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction(
    hackathon_service: HackathonService,
    mock_admin_case_input_data: AdminParticipantInputData,
    participant_repo_mock: Mock,
    team_repo_mock: Mock,
    tx_manager_mock: Mock,
) -> None:
    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = Team(name=mock_admin_case_input_data.team_name)
    participant_repo_mock.create.return_value = Participant(
        name=mock_admin_case_input_data.name,
        email=mock_admin_case_input_data.email,
        is_admin=True,
        team_id=team_repo_mock.create.return_value.id,
    )

    # This is the result of the callback passed to with_transaction
    tx_manager_mock.with_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    result = await hackathon_service.create_participant_and_team_in_transaction(mock_admin_case_input_data)

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_duplicate_team_name_err(
    hackathon_service: HackathonService, mock_admin_case_input_data: AdminParticipantInputData, tx_manager_mock: Mock
) -> None:
    # Mock an `Err` for duplicate team name returned from the passed callback to with_transaction. with_transaction
    # returns what the passed callback returns.
    tx_manager_mock.with_transaction.return_value = Err(DuplicateTeamNameError(mock_admin_case_input_data.team_name))

    result = await hackathon_service.create_participant_and_team_in_transaction(mock_admin_case_input_data)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == mock_admin_case_input_data.team_name


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_duplicate_email_err(
    hackathon_service: HackathonService, mock_admin_case_input_data: AdminParticipantInputData, tx_manager_mock: Mock
) -> None:
    # Mock an `Err` for duplicate email returned from the passed callback to with_transaction. with_transaction
    # returns what the passed callback returns.
    tx_manager_mock.with_transaction.return_value = Err(DuplicateEmailError(mock_admin_case_input_data.email))

    result = await hackathon_service.create_participant_and_team_in_transaction(mock_admin_case_input_data)

    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_admin_case_input_data.email


@pytest.mark.asyncio
async def test_register_admin_participant_general_exception(
    hackathon_service: HackathonService, mock_admin_case_input_data: AdminParticipantInputData, tx_manager_mock: Mock
) -> None:
    # Mock `with_transaction` to raise a general exception
    tx_manager_mock.with_transaction.return_value = Err(Exception("Test error"))

    result = await hackathon_service.create_participant_and_team_in_transaction(mock_admin_case_input_data)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_sufficient_capacity(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 18
    team_repo_mock.get_verified_registered_teams_count.return_value = 4

    # Call the admin case capacity check function
    result = await hackathon_service.check_capacity_register_admin_participant_case()

    # Assert the result is True (enough capacity)
    assert result is True


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_exact_limit(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 10
    team_repo_mock.get_verified_registered_teams_count.return_value = 10

    # Call the admin case capacity check function
    result = await hackathon_service.check_capacity_register_admin_participant_case()

    # Assert the result is False (capacity exactly reached)
    assert result is False


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_admin_case_with_exceeded_capacity(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 15
    team_repo_mock.get_verified_registered_teams_count.return_value = 11

    # Call the admin case capacity check function
    result = await hackathon_service.check_capacity_register_admin_participant_case()

    # Assert the result is False (capacity exceeded)
    assert result is False


@pytest.mark.asyncio
async def test_create_random_participant(
    hackathon_service: HackathonService,
    mock_random_case_input_data: RandomParticipantInputData,
    participant_repo_mock: Mock,
) -> None:
    # Mock successful `create` response for random participant.
    participant_repo_mock.create.return_value = Ok(
        Participant(
            name=mock_random_case_input_data.name,
            email=mock_random_case_input_data.email,
            is_admin=False,
            team_id=None,
        )
    )

    result = await hackathon_service.create_random_participant(mock_random_case_input_data)

    # Validate that the result is an `Ok` instance containing the participant object
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value[0], Participant)  # Check the first element is a Participant
    assert result.ok_value[0].name == mock_random_case_input_data.name
    assert result.ok_value[0].email == mock_random_case_input_data.email
    assert not result.ok_value[0].is_admin  # Ensure it is not an admin
    assert result.ok_value[1] is None  # Ensure the second element is None


@pytest.mark.asyncio
async def test_create_random_participant_duplicate_email_err(
    hackathon_service: HackathonService,
    mock_random_case_input_data: RandomParticipantInputData,
    participant_repo_mock: Mock,
) -> None:
    # Mock the `create` method to simulate a duplicate email error
    duplicate_email_error = DuplicateEmailError(mock_random_case_input_data.email)
    participant_repo_mock.create.return_value = Err(duplicate_email_error)

    result = await hackathon_service.create_random_participant(mock_random_case_input_data)

    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_random_case_input_data.email


@pytest.mark.asyncio
async def test_create_random_participant_general_exception(
    hackathon_service: HackathonService,
    mock_random_case_input_data: RandomParticipantInputData,
    participant_repo_mock: Mock,
) -> None:
    # Mock the `create` method to raise a general exception
    participant_repo_mock.create.return_value = Err(Exception("Test error"))

    result = await hackathon_service.create_random_participant(mock_random_case_input_data)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_random_case_with_sufficient_capacity(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 18
    team_repo_mock.get_verified_registered_teams_count.return_value = 4

    # Call the random case capacity check function
    result = await hackathon_service.check_capacity_register_random_participant_case()

    # Assert the result is True (enough capacity)
    assert result is True


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_random_case_with_exact_limit(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 10
    team_repo_mock.get_verified_registered_teams_count.return_value = 10

    # Call the random case capacity check function
    result = await hackathon_service.check_capacity_register_random_participant_case()

    # Assert the result is False (capacity exactly reached)
    assert result is True


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_capacity_random_case_with_exceeded_capacity(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 15
    team_repo_mock.get_verified_registered_teams_count.return_value = 11

    # Call the admin case capacity check function
    result = await hackathon_service.check_capacity_register_random_participant_case()

    # Assert the result is False (capacity exceeded)
    assert result is False


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_success(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    team_repo_mock: Mock,
    tx_manager_mock: Mock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:

    # Mocks update for team and participants repo
    team_repo_mock.update.return_value = Team(name=TEST_TEAM_NAME, is_verified=True)
    participant_repo_mock.update.return_value = Participant(
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        email_verified=True,
        is_admin=True,
        team_id=team_repo_mock.update.return_value.id,
    )

    # Result the callback passed to with_transaction
    tx_manager_mock.with_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    result = await hackathon_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)
    assert result.ok_value[0].email_verified == True
    assert result.ok_value[1].is_verified == True


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_team_not_found_error(
    hackathon_service: HackathonService,
    tx_manager_mock: Mock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:

    tx_manager_mock.with_transaction.return_value = Err(TeamNotFoundError())

    result = await hackathon_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNotFoundError)


@pytest.mark.asyncio
async def verify_admin_participant_and_team_in_transaction_general_error(
    hackathon_service: HackathonService,
    tx_manager_mock: Mock,
    mock_jwt_admin_user_verification: JwtParticipantVerificationData,
) -> None:

    tx_manager_mock.with_transaction.return_value = Err(Exception("Test error"))

    result = await hackathon_service.verify_admin_participant_and_team_in_transaction(
        jwt_data=mock_jwt_admin_user_verification
    )

    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_create_link_participant_duplicate_email_error(
    hackathon_service: HackathonService,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    participant_repo_mock: Mock,
    team_repo_mock: Mock,
    mock_jwt_user_registration: JwtParticipantInviteRegistrationData,
) -> None:

    # Mock successful `fetch_by_id` response for link participant's team.
    team_repo_mock.fetch_by_id.return_value = Ok(
        Team(id=ObjectId(mock_jwt_user_registration["team_id"]), name=mock_invite_link_case_input_data.team_name)
    )

    # Mock successful `create` response for link participant.
    participant_repo_mock.create.return_value = Err(DuplicateEmailError(mock_invite_link_case_input_data.email))

    result = await hackathon_service.create_invite_link_participant(
        mock_invite_link_case_input_data, mock_jwt_user_registration
    )

    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_invite_link_case_input_data.email


@pytest.mark.asyncio
async def test_register_link_participant_team_name_mismatch(
    hackathon_service: HackathonService,
    team_repo_mock: Mock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_jwt_user_registration: JwtParticipantInviteRegistrationData,
) -> None:
    # Modify the input_data to create a mismatch between the team names in the jwt and input data
    mock_invite_link_case_input_data.team_name = "modifiedteam"

    # Mock successful `fetch_by_id` response for link participant's team.
    team_repo_mock.fetch_by_id.return_value = Ok(
        Team(id=ObjectId(mock_jwt_user_registration["team_id"]), name=TEST_TEAM_NAME)
    )

    # Call the function under test
    result = await hackathon_service.create_invite_link_participant(
        mock_invite_link_case_input_data, mock_jwt_user_registration
    )

    # Check the err type
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamNameMissmatchError)


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_team_capacity_case_available_space(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock, mock_obj_id: str
) -> None:
    # Mock the get_number_registered_teammates() to return a number that is less that the MAX_NUMBER_OF_TEAM_MEMEBERS

    participant_repo_mock.get_number_registered_teammates.return_value = HackathonService.MAX_NUMBER_OF_TEAM_MEMBERS - 1

    result = await hackathon_service.check_team_capacity(mock_obj_id)

    assert result is True


@patch.object(HackathonService, "MAX_NUMBER_OF_TEAM_MEMBERS", 6)
@patch.object(HackathonService, "MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON", 12)
@pytest.mark.asyncio
async def test_check_team_capacity_case_capacity_exceeded(
    hackathon_service: HackathonService, participant_repo_mock: Mock, team_repo_mock: Mock, mock_obj_id: str
) -> None:

    participant_repo_mock.get_number_registered_teammates.return_value = HackathonService.MAX_NUMBER_OF_TEAM_MEMBERS

    result = await hackathon_service.check_team_capacity(mock_obj_id)

    assert result is False


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_success(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    mock_obj_id: str,
) -> None:

    participant_repo_mock.fetch_by_id.return_value = Ok(
        Participant(
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            email_verified=False,
            is_admin=False,
            team_id=None,
            last_sent_email=PARTICIPANT_LAST_SENT_EMAIL_VALID_RANGE,
        )
    )
    result = await hackathon_service.check_send_verification_email_rate_limit(participant_id=mock_obj_id)
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, bool)
    assert result.ok_value == True


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_limit_reached(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    mock_obj_id: str,
) -> None:

    participant_repo_mock.fetch_by_id.return_value = Ok(
        Participant(
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            email_verified=False,
            is_admin=False,
            team_id=None,
            last_sent_email=PARTICIPANT_LAST_SENT_EMAIL_INVALID_RANGE,
        )
    )

    result = await hackathon_service.check_send_verification_email_rate_limit(participant_id=mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, bool)
    assert result.ok_value == False


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_without_last_sent_email(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    mock_obj_id: str,
) -> None:

    participant_repo_mock.fetch_by_id.return_value = Ok(
        Participant(
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            email_verified=False,
            is_admin=False,
            team_id=None,
            last_sent_email=None,
        )
    )

    result = await hackathon_service.check_send_verification_email_rate_limit(participant_id=mock_obj_id)

    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, bool)
    assert result.ok_value == True


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_already_verified(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    mock_obj_id: str,
) -> None:

    participant_repo_mock.fetch_by_id.return_value = Ok(
        Participant(
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            email_verified=True,
            is_admin=False,
            team_id=None,
            last_sent_email=None,
        )
    )

    result = await hackathon_service.check_send_verification_email_rate_limit(participant_id=mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantAlreadyVerifiedError)


@pytest.mark.asyncio
async def test_check_send_verification_email_rate_limit_participant_not_found(
    hackathon_service: HackathonService,
    participant_repo_mock: Mock,
    mock_obj_id: str,
) -> None:

    participant_repo_mock.fetch_by_id.return_value = Err(ParticipantNotFoundError())

    result = await hackathon_service.check_send_verification_email_rate_limit(participant_id=mock_obj_id)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)
