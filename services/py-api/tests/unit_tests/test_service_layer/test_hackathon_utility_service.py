from typing import cast
import pytest
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.service.hackathon.team_service import TeamService
from tests.unit_tests.conftest import (
    ParticipantRepoMock,
    TeamRepoMock,
    FeatureSwitchRepoMock,
    TeamServiceMock,
)


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
