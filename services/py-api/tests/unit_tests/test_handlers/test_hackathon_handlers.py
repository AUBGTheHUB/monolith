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
from src.service.hackathon.hackathon_service import HackathonService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_NAME
from tests.unit_tests.conftest import HackathonServiceMock


@pytest.fixture
def hackathon_handlers(hackathon_service_mock: HackathonServiceMock) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(cast(HackathonService, hackathon_service_mock))


@pytest.mark.asyncio
async def test_delete_participant_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: Mock,
    mock_obj_id: str,
    mock_admin_participant: Participant,
) -> None:

    # Given
    # Deleting an admin participant has no difference from deleting a random participant
    hackathon_service_mock.delete_participant.return_value = Ok(mock_admin_participant)

    # When
    resp = await hackathon_handlers.delete_participant(mock_obj_id)

    # Then
    # Check that `delete_participant` was awaited once with the expected object_id
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_obj_id)
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantDeletedResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.id == mock_obj_id
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_participant_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers, hackathon_service_mock: Mock, mock_obj_id: str
) -> None:

    # Given
    # Mock delete_participant to return a ParticipantNotFoundError
    hackathon_service_mock.delete_participant.return_value = Err(ParticipantNotFoundError())

    # When
    resp = await hackathon_handlers.delete_participant(mock_obj_id)

    # Then
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_obj_id)
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_participant_general_exception(
    hackathon_handlers: HackathonManagementHandlers, hackathon_service_mock: Mock, mock_obj_id: str
) -> None:

    # Given
    # Mock delete_participant to return a General Exception
    hackathon_service_mock.delete_participant.return_value = Err(Exception())

    # When
    resp = await hackathon_handlers.delete_participant(mock_obj_id)

    # Then
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_obj_id)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_delete_team_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: Mock,
    mock_verified_team: Team,
    mock_obj_id: str,
) -> None:

    # Given
    # Deleting a verified team has no difference from deleting an unverified team
    hackathon_service_mock.delete_team.return_value = Ok(mock_verified_team)

    # When
    # Call the handler
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then
    # Check that `delete_team` was awaited once with the expected object_id
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TeamDeletedResponse)
    assert resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.response_model.team.id == mock_obj_id
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_team_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: Mock,
    mock_obj_id: str,
) -> None:

    # Given
    # Mock delete_team to return a TeamNotFoundError
    hackathon_service_mock.delete_team.return_value = Err(TeamNotFoundError())

    # When
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: Mock,
    mock_obj_id: str,
) -> None:

    # Given
    # Mock delete_team to return a General Exception
    hackathon_service_mock.delete_team.return_value = Err(Exception())

    # When
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)
    # Assert that the response is unsuccessful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
