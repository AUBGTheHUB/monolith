from unittest.mock import patch, MagicMock, AsyncMock
from unittest.mock import Mock

import pytest
from result import Ok, Err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import (
    DuplicateTeamNameError,
    DuplicateEmailError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    ParticipantNotFoundError,
)
from src.server.schemas.jwt_schemas.schemas import JwtParticipantInviteRegistrationData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
)
from src.service.participants_registration_service import ParticipantRegistrationService
from src.utils import JwtUtility


@pytest.fixture
def p_reg_service(hackathon_service_mock: Mock) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(hackathon_service_mock)


@pytest.mark.asyncio
async def test_register_admin_participant_success(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: MagicMock,
    participant_repo_mock: Mock,
    mock_admin_participant: Participant,
    mock_unverified_team: Team,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True
    # Mock no err when sending verification email
    hackathon_service_mock.send_verification_email = AsyncMock(return_value=None)

    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = mock_unverified_team
    participant_repo_mock.create.return_value = mock_admin_participant

    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Check if the send_verification_email has been called and awaited once
    hackathon_service_mock.send_verification_email.assert_awaited_once_with(
        participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
    )

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_team_name_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate team name
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateTeamNameError(mock_admin_case_input_data.team_name)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == mock_admin_case_input_data.team_name


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_email_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate email err
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateEmailError(mock_admin_case_input_data.email)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_admin_case_input_data.email


@pytest.mark.asyncio
async def test_register_admin_participant_general_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = True

    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_admin_participant_with_hackathon_cap_exceeded(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: MagicMock,
    mock_unverified_team: Team,
    mock_admin_participant: Participant,
    participant_repo_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = False

    # Everything else is as expected
    team_repo_mock.create.return_value = mock_unverified_team
    participant_repo_mock.create.return_value = mock_admin_participant

    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_admin_participant_order_of_operations(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case.return_value = False

    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data, background_tasks)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_success(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    participant_repo_mock: Mock,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock no err when sending verification email
    hackathon_service_mock.send_verification_email = AsyncMock(return_value=None)

    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = mock_random_participant

    hackathon_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)

    # Check if the send_verification_email has been called and awaited once
    hackathon_service_mock.send_verification_email.assert_awaited_once_with(
        participant=result.ok_value[0], background_tasks=background_tasks
    )

    # Validate that the result is an `Ok` instance containing the created participant
    assert isinstance(result, Ok)
    participant, team = result.ok_value  # Unpack the tuple

    assert isinstance(participant, Participant)
    assert participant.name == mock_random_case_input_data.name
    assert participant.email == mock_random_case_input_data.email
    assert not participant.is_admin  # Ensure it is not an admin
    assert team is None  # Ensure second element is None since teams are assigned later


@pytest.mark.asyncio
async def test_register_random_participant_duplicate_email_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True

    # Mock `create_random_participant` to return an `Err` for duplicate email err
    hackathon_service_mock.create_random_participant.return_value = Err(
        DuplicateEmailError(mock_random_case_input_data.email)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_random_case_input_data.email


# This test is also valid for admin participants
@pytest.mark.asyncio
async def test_register_random_participant_send_verification_email_failure_email_body_generation_failed(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: MagicMock,
    participant_repo_mock: Mock,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock err when sending verification email (email body generation)
    hackathon_service_mock.send_verification_email.return_value = Err(ValueError("Test Error"))

    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = mock_random_participant

    hackathon_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)
    # Check that the result is an `Err` with `ValueError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


# This test is also valid for admin participants
@pytest.mark.asyncio
async def test_register_random_participant_send_verification_email_failure_participant_deleted_before_sending_email(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    background_tasks: MagicMock,
    participant_repo_mock: Mock,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock err when sending verification email (email body generation)
    hackathon_service_mock.send_verification_email.return_value = Err(ParticipantNotFoundError("Test Error"))

    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = mock_random_participant

    hackathon_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)
    # Check that the result is an `Err` with `ParticipantNotFoundError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_register_random_participant_general_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True

    # Mock `create_random_participant` to raise a general exception
    hackathon_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_random_participant_with_hackathon_cap_exceeded(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    participant_repo_mock: Mock,
    background_tasks: MagicMock,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = False

    # Everything else is as expected
    participant_repo_mock.create.return_value = mock_random_participant

    hackathon_service_mock.create_random_participant.return_value = Ok(participant_repo_mock.create.return_value)

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_order_of_operations(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = False

    # Mock `create_random_participant` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    hackathon_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data, background_tasks)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_register_link_participant_success(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    participant_repo_mock: Mock,
    background_tasks: MagicMock,
    mock_invite_participant: Participant,
    mock_verified_team: Team,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_jwt_user_registration: JwtParticipantInviteRegistrationData,
) -> None:
    # Mock team has available space
    hackathon_service_mock.check_team_capacity.return_value = True
    # Mock no err when sending verification email
    hackathon_service_mock.send_successful_registration_email = Mock(return_value=None)

    # Cereat a mock jwt_token to pass to the service method
    jwt_token = JwtUtility.encode_data(data=mock_jwt_user_registration)

    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = mock_verified_team
    participant_repo_mock.create.return_value = mock_invite_participant

    hackathon_service_mock.create_invite_link_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(
        mock_invite_link_case_input_data, jwt_token, background_tasks
    )

    # Check if the send_verification_email has been called and awaited once
    hackathon_service_mock.send_successful_registration_email.assert_called_once_with(
        participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks
    )

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)
    assert result.ok_value[0].team_id == result.ok_value[1].id


@patch.dict("os.environ", {"SECRET_KEY": "abcdefghijklmnopqrst"})
@pytest.mark.asyncio
async def test_register_link_participant_capacity_exceeded(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    background_tasks: MagicMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_jwt_user_registration: JwtParticipantInviteRegistrationData,
) -> None:
    # Mock the check to return Team Capacity Exceeded Error
    hackathon_service_mock.check_team_capacity.return_value = False

    # Cereat a mock jwt_token to pass to the service method
    jwt_token = JwtUtility.encode_data(data=mock_jwt_user_registration)

    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(
        mock_invite_link_case_input_data, jwt_token, background_tasks
    )

    # Check the err type
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamCapacityExceededError)
