from unittest.mock import AsyncMock, patch
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
)
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserRegistration
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
    participant_repo_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = Team(name=mock_admin_case_input_data.team_name)
    participant_repo_mock.create.return_value = Participant(
        name=mock_admin_case_input_data.name,
        email=mock_admin_case_input_data.email,
        is_admin=True,
        team_id=team_repo_mock.create.return_value.id,
    )

    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_team_name_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate team name
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateTeamNameError(mock_admin_case_input_data.team_name)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == mock_admin_case_input_data.team_name


@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_email_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate email err
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateEmailError(mock_admin_case_input_data.email)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_admin_case_input_data.email


@pytest.mark.asyncio
async def test_register_admin_participant_general_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_admin_participant_with_hackathon_cap_exceeded(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    team_repo_mock: Mock,
    participant_repo_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=False)

    # Everything else is as expected
    team_repo_mock.create.return_value = Team(name=mock_admin_case_input_data.team_name)
    participant_repo_mock.create.return_value = Participant(
        name=mock_admin_case_input_data.name,
        email=mock_admin_case_input_data.email,
        is_admin=True,
        team_id=team_repo_mock.create.return_value.id,
    )

    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_admin_participant_order_of_operations(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_admin_case_input_data: AdminParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=False)

    # Mock `create_participant_and_team_in_transaction` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_admin_case_input_data)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_success(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    participant_repo_mock: Mock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case = AsyncMock(return_value=True)

    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    participant_repo_mock.create.return_value = Participant(
        name=mock_random_case_input_data.name,
        email=mock_random_case_input_data.email,
        is_admin=False,
        team_id=None,
    )

    hackathon_service_mock.create_random_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, None)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data)

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
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case = AsyncMock(return_value=True)

    # Mock `create_random_participant` to return an `Err` for duplicate email err
    hackathon_service_mock.create_random_participant.return_value = Err(
        DuplicateEmailError(mock_random_case_input_data.email)
    )

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_random_case_input_data.email


@pytest.mark.asyncio
async def test_register_random_participant_general_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case = AsyncMock(return_value=True)

    # Mock `create_random_participant` to raise a general exception
    hackathon_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data)

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_register_random_participant_with_hackathon_cap_exceeded(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    participant_repo_mock: Mock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case = AsyncMock(return_value=False)

    # Everything else is as expected
    participant_repo_mock.create.return_value = Participant(
        name=mock_random_case_input_data.name,
        email=mock_random_case_input_data.email,
        is_admin=False,
        team_id=None,
    )

    hackathon_service_mock.create_random_participant.return_value = Ok(participant_repo_mock.create.return_value)

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data)

    # Check that the result is an `Err` of type HackathonCapacityExceededError
    assert isinstance(result, Err)
    assert isinstance(result.err_value, HackathonCapacityExceededError)


@pytest.mark.asyncio
async def test_register_random_participant_order_of_operations(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_random_case_input_data: RandomParticipantInputData,
) -> None:
    # Mock full hackathon
    hackathon_service_mock.check_capacity_register_random_participant_case = AsyncMock(return_value=False)

    # Mock `create_random_participant` to raise a general exception
    # This is in order to show that we should return the first faced err and that we check first the hackathon capacity
    # It should have no effect to the expected result of the test
    hackathon_service_mock.create_random_participant.return_value = Err(Exception("Test error"))

    # Call the function under test
    result = await p_reg_service.register_random_participant(mock_random_case_input_data)

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
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_jwt_user_registration: JwtUserRegistration,
) -> None:
    # Mock team has available space
    hackathon_service_mock.check_team_capacity = AsyncMock(return_value=True)

    # Cereat a mock jwt_token to pass to the service method
    jwt_token = JwtUtility.encode_data(data=mock_jwt_user_registration)

    # Mock successful `create` responses for team and participant. These are the operations inside the passed callback
    # to with_transaction
    team_repo_mock.create.return_value = Team(
        id=mock_jwt_user_registration["team_id"], name=mock_invite_link_case_input_data.team_name
    )
    participant_repo_mock.create.return_value = Participant(
        name=mock_invite_link_case_input_data.name,
        email=mock_invite_link_case_input_data.email,
        is_admin=False,
        team_id=mock_jwt_user_registration["team_id"],
    )

    hackathon_service_mock.create_invite_link_participant.return_value = Ok(
        (participant_repo_mock.create.return_value, team_repo_mock.create.return_value)
    )

    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(mock_invite_link_case_input_data, jwt_token)

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
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_jwt_user_registration: JwtUserRegistration,
) -> None:
    # Mock the check to return Team Capacity Exceeded Error
    hackathon_service_mock.check_team_capacity = AsyncMock(return_value=False)

    # Cereat a mock jwt_token to pass to the service method
    jwt_token = JwtUtility.encode_data(data=mock_jwt_user_registration)

    # Call the function under test
    result = await p_reg_service.register_invite_link_participant(mock_invite_link_case_input_data, jwt_token)

    # Check the err type
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TeamCapacityExceededError)
