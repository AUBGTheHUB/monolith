from typing import cast
from unittest.mock import Mock
import pytest
from result import Err, Ok
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import ParticipantNotFoundError, TeamNotFoundError
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantDeletedResponse,
    Response,
    TeamDeletedResponse,
)
from starlette import status
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.team_service import TeamService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_NAME
from tests.unit_tests.conftest import HackathonUtilityServiceMock, ParticipantServiceMock, TeamServiceMock


@pytest.fixture
def hackathon_handlers(
    hackathon_utility_service_mock: HackathonUtilityServiceMock,
    participant_service_mock: ParticipantServiceMock,
    team_service_mock: TeamServiceMock,
) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(
        cast(HackathonUtilityService, hackathon_utility_service_mock),
        cast(ParticipantService, participant_service_mock),
        cast(TeamService, team_service_mock),
    )


@pytest.mark.asyncio
async def test_delete_participant_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_utility_service_mock: Mock,
    obj_id_mock: str,
    admin_participant_mock: Participant,
) -> None:
    # Given
    # Deleting an admin participant has no difference from deleting a random participant
    hackathon_utility_service_mock.delete_participant.return_value = Ok(admin_participant_mock)

    # When
    resp = await hackathon_handlers.delete_participant(obj_id_mock)

    # Then
    # Check that `delete_participant` was awaited once with the expected object_id
    hackathon_utility_service_mock.delete_participant.assert_awaited_once_with(obj_id_mock)
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantDeletedResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.id == obj_id_mock
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_participant_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers, hackathon_utility_service_mock: Mock, obj_id_mock: str
) -> None:
    # Given
    # Mock delete_participant to return a ParticipantNotFoundError
    hackathon_utility_service_mock.delete_participant.return_value = Err(ParticipantNotFoundError())

    # When
    resp = await hackathon_handlers.delete_participant(obj_id_mock)

    # Then
    hackathon_utility_service_mock.delete_participant.assert_awaited_once_with(obj_id_mock)
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_participant_general_exception(
    hackathon_handlers: HackathonManagementHandlers, hackathon_utility_service_mock: Mock, obj_id_mock: str
) -> None:
    # Given
    # Mock delete_participant to return a General Exception
    hackathon_utility_service_mock.delete_participant.return_value = Err(Exception())

    # When
    resp = await hackathon_handlers.delete_participant(obj_id_mock)

    # Then
    hackathon_utility_service_mock.delete_participant.assert_awaited_once_with(obj_id_mock)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_delete_team_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_utility_service_mock: Mock,
    verified_team_mock: Team,
    obj_id_mock: str,
) -> None:
    # Given
    # Deleting a verified team has no difference from deleting an unverified team
    hackathon_utility_service_mock.delete_team.return_value = Ok(verified_team_mock)

    # When
    # Call the handler
    resp = await hackathon_handlers.delete_team(obj_id_mock)

    # Then
    # Check that `delete_team` was awaited once with the expected object_id
    hackathon_utility_service_mock.delete_team.assert_awaited_once_with(obj_id_mock)

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TeamDeletedResponse)
    assert resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.response_model.team.id == obj_id_mock
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_team_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_utility_service_mock: Mock,
    obj_id_mock: str,
) -> None:
    # Given
    # Mock delete_team to return a TeamNotFoundError
    hackathon_utility_service_mock.delete_team.return_value = Err(TeamNotFoundError())

    # When
    resp = await hackathon_handlers.delete_team(obj_id_mock)

    # Then
    hackathon_utility_service_mock.delete_team.assert_awaited_once_with(obj_id_mock)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_utility_service_mock: Mock,
    obj_id_mock: str,
) -> None:
    # Given
    # Mock delete_team to return a General Exception
    hackathon_utility_service_mock.delete_team.return_value = Err(Exception())

    # When
    resp = await hackathon_handlers.delete_team(obj_id_mock)

    # Then
    hackathon_utility_service_mock.delete_team.assert_awaited_once_with(obj_id_mock)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
