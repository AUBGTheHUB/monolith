from unittest.mock import Mock
from unittest.mock import AsyncMock
import pytest
from bson import ObjectId
from result import Ok, Err

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.service.participants_service import ParticipantService


@pytest.fixture
def participant_service(participant_repo_mock: Mock, team_repo_mock: Mock, tx_manager_mock: Mock) -> ParticipantService:
    return ParticipantService(participant_repo_mock, team_repo_mock, tx_manager_mock)


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_success(
    participant_service: ParticipantService,
    team_repo_mock: Mock,
    participant_repo_mock: Mock,
    mock_input_data: ParticipantRequestBody,
) -> None:
    # Mock successful `create` responses for team and participant
    team_repo_mock.create.return_value = Ok(Team(name=mock_input_data.team_name))
    participant_repo_mock.create.return_value = Ok(
        Participant(
            name=mock_input_data.name,
            email=mock_input_data.email,
            is_admin=True,
            team_id=team_repo_mock.create.return_value.ok_value.id,
        )
    )

    # Call the function under test
    result = await participant_service._create_participant_and_team_in_transaction(mock_input_data)

    # Assert `create` calls were awaited once for each repository with expected arguments
    team_repo_mock.create.assert_awaited_once_with(mock_input_data, None)
    participant_repo_mock.create.assert_awaited_once_with(
        mock_input_data, None, team_id=team_repo_mock.create.return_value.ok_value.id
    )

    # Check that the result is an `Ok` containing both the participant and team objects
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_team_duplicate_name_error(
    participant_service: ParticipantService,
    team_repo_mock: Mock,
    participant_repo_mock: Mock,
    mock_input_data: ParticipantRequestBody,
) -> None:
    # Mock `team_repo.create` to return an `Err` for duplicate team name
    team_repo_mock.create.return_value = Err(DuplicateTeamNameError(mock_input_data.team_name))

    # Call the function under test
    result = await participant_service._create_participant_and_team_in_transaction(mock_input_data)

    # Assert only the team `create` method was called, as the participant creation should be skipped
    team_repo_mock.create.assert_awaited_once_with(mock_input_data, None)
    participant_repo_mock.create.assert_not_awaited()

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == mock_input_data.team_name


@pytest.mark.asyncio
async def test_create_participant_and_team_in_transaction_participant_duplicate_email_error(
    participant_service: ParticipantService,
    team_repo_mock: Mock,
    participant_repo_mock: Mock,
    mock_input_data: ParticipantRequestBody,
) -> None:
    # Mock successful team creation and simulate a duplicate email error in participant creation
    team_repo_mock.create.return_value = Ok(Team(name=mock_input_data.team_name))
    participant_repo_mock.create.return_value = Err(DuplicateEmailError(mock_input_data.email))

    # Call the function under test
    result = await participant_service._create_participant_and_team_in_transaction(mock_input_data)

    # Assert both `create` calls were awaited with the expected arguments
    team_repo_mock.create.assert_awaited_once_with(mock_input_data, None)
    participant_repo_mock.create.assert_awaited_once_with(
        mock_input_data, None, team_id=team_repo_mock.create.return_value.ok_value.id
    )

    # Check that the result is an `Err` with `DuplicateEmailError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateEmailError)
    assert str(result.err_value) == mock_input_data.email


@pytest.mark.asyncio
async def test_register_admin_participant_success(
    participant_service: ParticipantService, tx_manager_mock: AsyncMock, mock_input_data: ParticipantRequestBody
) -> None:
    # Mock transaction manager to call the `_create_participant_and_team_in_transaction` function
    tx_manager_mock.with_transaction.return_value = Ok(
        (
            Participant(name=mock_input_data.name, email=mock_input_data.email, is_admin=True, team_id=ObjectId()),
            Team(name=mock_input_data.team_name),
        )
    )

    # Mocks the behaviour of capacity check 2
    participant_service._check_capacity_register_admin_participant_case = AsyncMock(return_value=True)
    # Call `register_admin_participant`
    result = await participant_service.register_admin_participant(mock_input_data)

    # Check that `with_transaction` was awaited once
    tx_manager_mock.with_transaction.assert_awaited_once_with(
        participant_service._create_participant_and_team_in_transaction, mock_input_data
    )

    # Verify the result is an `Ok` with a tuple containing participant and team
    assert isinstance(result, Ok)
    assert isinstance(result.ok_value, tuple)
    assert isinstance(result.ok_value[0], Participant)
    assert isinstance(result.ok_value[1], Team)


@pytest.mark.asyncio
async def test_register_admin_participant_general_exception(
    participant_service: ParticipantService, tx_manager_mock: AsyncMock, mock_input_data: ParticipantRequestBody
) -> None:
    # Mock `with_transaction` to raise a general exception
    tx_manager_mock.with_transaction.return_value = Err(Exception("Test error"))

    # Mocks the behaviour of capacity check 2
    participant_service._check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Call `register_admin_participant`
    result = await participant_service.register_admin_participant(mock_input_data)

    # Check that `with_transaction` was awaited once
    tx_manager_mock.with_transaction.assert_awaited_once_with(
        participant_service._create_participant_and_team_in_transaction, mock_input_data
    )

    # Verify the result is an `Err` containing a general Exception
    assert isinstance(result, Err)
    assert isinstance(result.err_value, Exception)
    assert str(result.err_value) == "Test error"


@pytest.mark.asyncio
async def test_check_capacity_with_sufficient_capacity(
    participant_service: ParticipantService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 18
    team_repo_mock.get_verified_registered_teams_count.return_value = 4

    # Mock MAX_NUMBER_OF_TEAM_MEMBERS and MAX_NUMBER_OF_TEAMS_IN_HACKATHON
    team_repo_mock.MAX_NUMBER_OF_TEAM_MEMBERS = 6
    team_repo_mock.MAX_NUMBER_OF_TEAMS_IN_HACKATHON = 12

    # Call the capacity check function
    result = await participant_service._check_capacity_register_admin_participant_case()

    # Assert the result is True (enough capacity)
    assert result is True


@pytest.mark.asyncio
async def test_check_capacity_with_exact_limit(
    participant_service: ParticipantService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 10
    team_repo_mock.get_verified_registered_teams_count.return_value = 10

    # Mock MAX_NUMBER_OF_TEAM_MEMBERS and MAX_NUMBER_OF_TEAMS_IN_HACKATHON
    team_repo_mock.MAX_NUMBER_OF_TEAM_MEMBERS = 6
    team_repo_mock.MAX_NUMBER_OF_TEAMS_IN_HACKATHON = 12

    # Call the capacity check function
    result = await participant_service._check_capacity_register_admin_participant_case()

    # Assert the result is False (capacity exactly reached)
    assert result is False


@pytest.mark.asyncio
async def test_check_capacity_with_exceeded_capacity(
    participant_service: ParticipantService, participant_repo_mock: Mock, team_repo_mock: Mock
) -> None:
    # Mock repository methods to return controlled values
    participant_repo_mock.get_verified_random_participants_count.return_value = 15
    team_repo_mock.get_verified_registered_teams_count.return_value = 11

    # Mock MAX_NUMBER_OF_TEAM_MEMBERS and MAX_NUMBER_OF_TEAMS_IN_HACKATHON
    team_repo_mock.MAX_NUMBER_OF_TEAM_MEMBERS = 6
    team_repo_mock.MAX_NUMBER_OF_TEAMS_IN_HACKATHON = 12

    # Call the capacity check function
    result = await participant_service._check_capacity_register_admin_participant_case()

    # Assert the result is False (capacity exceeded)
    assert result is False
