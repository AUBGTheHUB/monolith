from typing import cast
import pytest
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    MongoTransactionManagerMock,
    TeamServiceMock,
    ParticipantServiceMock,
)
from src.service.hackathon.team_service import TeamService
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.constants import MAX_NUMBER_OF_TEAM_MEMBERS


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
