from typing import cast
from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest
from fastapi import BackgroundTasks
from result import Ok, Err
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    ParticipantNotFoundError,
    TeamCapacityExceededError,
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
from src.service.hackathon.registration_service import RegistrationService
from src.service.hackathon.team_service import TeamService
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData
from src.service.jwt_utils.codec import JwtUtility
from tests.unit_tests.conftest import (
    HackathonServiceMock,
    TeamRepoMock,
    ParticipantRepoMock,
    BackgroundTasksMock,
    ParticipantServiceMock,
    TeamServiceMock,
    HackathonMailServiceMock,
    AdminTeamServiceMock,
)


@pytest.fixture
def p_reg_service(
    hackathon_utility_service_mock: HackathonServiceMock,
    jwt_utility_mock: JwtUtility,
    participant_service_mock: ParticipantServiceMock,
    team_service_mock: TeamServiceMock,
    hackathon_mail_service_mock: HackathonMailServiceMock,
    admin_team_service_mock: AdminTeamServiceMock,
) -> RegistrationService:
    return RegistrationService(
        cast(AdminTeamService, admin_team_service_mock),
        cast(ParticipantService, participant_service_mock),
        cast(TeamService, team_service_mock),
        cast(HackathonUtilityService, hackathon_utility_service_mock),
        cast(HackathonMailService, hackathon_mail_service_mock),
        jwt_utility_mock,
    )


@pytest.mark.asyncio
async def test_register_admin_participant_success(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    participant_repo_mock: ParticipantRepoMock,
    admin_participant_mock: Participant,
    unverified_team_mock: Team,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    # Mock no err when sending verification email
    hackathon_utility_service_mock.send_verification_email = AsyncMock(return_value=None)
    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = unverified_team_mock
    participant_repo_mock.create.return_value = admin_participant_mock

    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check if the send_verification_email has been called and awaited once
    hackathon_utility_service_mock.send_verification_email.assert_awaited_once_with(
        participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks_mock
    )

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_team_name_error(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate team name
    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateTeamNameError(admin_case_input_data_mock.team_name)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == admin_case_input_data_mock.team_name


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_email_error(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate email err
    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateEmailError(str(admin_case_input_data_mock.email))
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == admin_case_input_data_mock.email


@pytest.mark.asyncio
async def test_register_admin_participant_general_error(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = True
    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        Exception("Test error")
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_admin_participant_with_hackathon_cap_exceeded(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    unverified_team_mock: Team,
    admin_participant_mock: Participant,
    participant_repo_mock: ParticipantRepoMock,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = False
    # Everything else is as expected
    team_repo_mock.create.return_value = unverified_team_mock
    participant_repo_mock.create.return_value = admin_participant_mock
    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_admin_participant_order_of_operations(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    admin_case_input_data_mock: AdminParticipantInputData,
) -> None:
    # Given
    # Mock full hackathon
    hackathon_utility_service_mock.check_capacity_register_admin_participant_case.return_value = False
    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    hackathon_utility_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        Exception("Test error")
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_admin_participant(
        admin_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_success(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock no err when sending verification email
    hackathon_utility_service_mock.send_verification_email = AsyncMock(return_value=None)
    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = random_participant_mock
    participant_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check if the send_verification_email has been called and awaited once
    hackathon_utility_service_mock.send_verification_email.assert_awaited_once_with(
        participant=result.ok_value[0], background_tasks=background_tasks_mock
    )
    # Validate that the result is an `Ok` instance containing the created participant
    assert isinstance(result, Ok)
    participant, team = result.ok_value  # Unpack the tuple
    assert isinstance(participant, Participant)
    assert participant.name == random_case_input_data_mock.name
    assert participant.email == random_case_input_data_mock.email
    assert not participant.is_admin  # Ensure it is not an admin
    assert team is None  # Ensure second element is None since teams are assigned later


@pytest.mark.asyncio
async def test_register_random_participant_duplicate_email_error(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock `create_random_participant` to return an `Err` for duplicate email err
    participant_service_mock.create_random_participant.return_value = Err(
        DuplicateEmailError(str(random_case_input_data_mock.email))
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == random_case_input_data_mock.email


# This test is also valid for admin participants
@pytest.mark.asyncio
async def test_register_random_participant_send_verification_email_failure_email_body_generation_failed(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock err when sending verification email (email body generation)
    hackathon_utility_service_mock.send_verification_email.return_value = Err(ValueError("Test Error"))
    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = random_participant_mock
    participant_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` with `ValueError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


# This test is also valid for admin participants
@pytest.mark.asyncio
async def test_register_random_participant_send_verification_email_failure_participant_deleted_before_sending_email(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    team_repo_mock: TeamRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    participant_repo_mock: ParticipantRepoMock,
    random_participant_mock: Participant,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock err when sending verification email (email body generation)
    hackathon_utility_service_mock.send_verification_email.return_value = Err(ParticipantNotFoundError("Test Error"))
    # Mock successful `create` responses for participant.
    participant_repo_mock.create.return_value = random_participant_mock
    participant_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` with `ParticipantNotFoundError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ParticipantNotFoundError)


@pytest.mark.asyncio
async def test_register_random_participant_general_error(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock not full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = True
    # Mock `create_random_participant` to raise a general exception
    participant_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_random_participant_with_hackathon_cap_exceeded(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    random_participant_mock: Participant,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = False
    # Everything else is as expected
    participant_repo_mock.create.return_value = random_participant_mock
    participant_service_mock.create_random_participant.return_value = Ok(participant_repo_mock.create.return_value)

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_order_of_operations(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    random_case_input_data_mock: RandomParticipantInputData,
) -> None:
    # Given
    # Mock full hackathon
    hackathon_utility_service_mock.check_capacity_register_random_participant_case.return_value = False
    # Mock `create_random_participant` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    participant_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # When
    # Call the function under test
    result = await p_reg_service.register_random_participant(
        random_case_input_data_mock, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_link_participant_success(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    participant_service_mock: ParticipantServiceMock,
    team_repo_mock: TeamRepoMock,
    participant_repo_mock: ParticipantRepoMock,
    background_tasks_mock: BackgroundTasksMock,
    invite_participant_mock: Participant,
    verified_team_mock: Team,
    invite_link_case_input_data_mock: InviteLinkParticipantInputData,
    jwt_user_registration_mock: JwtParticipantInviteRegistrationData,
    jwt_utility_mock: JwtUtility,
) -> None:
    # Given
    # Mock team has available space
    hackathon_utility_service_mock.check_team_capacity.return_value = True
    # Mock no err when sending verification email
    hackathon_utility_service_mock.send_successful_registration_email = Mock(return_value=None)
    # Cereat a mock jwt_token to pass to the service method
    jwt_token = jwt_utility_mock.encode_data(data=jwt_user_registration_mock)
    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = verified_team_mock
    participant_repo_mock.create.return_value = invite_participant_mock
    participant_service_mock.create_invite_link_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # When
    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(
        invite_link_case_input_data_mock, jwt_token, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check if the send_verification_email has been called and awaited once
    hackathon_utility_service_mock.send_successful_registration_email.assert_called_once_with(
        participant=result.ok_value[0], team=result.ok_value[1], background_tasks=background_tasks_mock
    )
    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)
    assert result.ok_value[0].team_id == result.ok_value[1].id


@pytest.mark.asyncio
async def test_register_link_participant_capacity_exceeded(
    p_reg_service: RegistrationService,
    hackathon_utility_service_mock: HackathonServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    invite_link_case_input_data_mock: InviteLinkParticipantInputData,
    jwt_user_registration_mock: JwtParticipantInviteRegistrationData,
    jwt_utility_mock: JwtUtility,
) -> None:
    # Given
    # Mock the check to return Team Capacity Exceeded Error
    hackathon_utility_service_mock.check_team_capacity.return_value = False
    # Create a mock jwt_token to pass to the service method
    jwt_token = jwt_utility_mock.encode_data(data=jwt_user_registration_mock)

    # When
    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(
        invite_link_case_input_data_mock, jwt_token, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then
    # Check the err type
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamCapacityExceededError)
