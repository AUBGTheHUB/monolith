from typing import cast
import pytest
from src.service.hackathon.admin_team_service import AdminTeamService
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    MongoTransactionManagerMock,
)
from src.server.schemas.request_schemas.hackathon.schemas import (
    AdminParticipantInputData,
)
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from result import Ok, Err
from src.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    TeamNotFoundError,
)
from src.service.jwt_utils.schemas import JwtParticipantVerificationData


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
