from typing import cast

import pytest
from result import Err, Ok
from starlette import status

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import ParticipantNotFoundError, TeamNotFoundError
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantDeletedResponse,
    Response,
    TeamDeletedResponse,
)
from src.service.hackathon_service import HackathonService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_NAME
from tests.unit_tests.conftest import HackathonServiceMock


@pytest.fixture
def hackathon_handlers(hackathon_service_mock: HackathonServiceMock) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(service=cast(HackathonService, hackathon_service_mock))


@pytest.mark.asyncio
async def test_delete_participant_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: HackathonServiceMock,
    mock_random_participant: Participant,
) -> None:
    # Given an OK result from 'delete_participant'
    # Note: Deleting an admin participant has no difference from deleting a random participant
    hackathon_service_mock.delete_participant.return_value = Ok(mock_random_participant)

    # When we call the handler
    resp = await hackathon_handlers.delete_participant(mock_random_participant.id)

    # Then the delete_participant should have been awaited once with the expected object_id
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_random_participant.id)

    # And the response is a 200 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantDeletedResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.id == mock_random_participant.id
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_participant_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers, hackathon_service_mock: HackathonServiceMock, mock_obj_id: str
) -> None:
    # Given a ParticipantNotFoundError from delete_participant
    hackathon_service_mock.delete_participant.return_value = Err(ParticipantNotFoundError())

    # When we call the handler
    resp = await hackathon_handlers.delete_participant(mock_obj_id)

    # Then the delete_participant should have been awaited once with the expected object_id
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_obj_id)

    # And the response is a 404 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified participant was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_participant_general_exception(
    hackathon_handlers: HackathonManagementHandlers, hackathon_service_mock: HackathonServiceMock, mock_obj_id: str
) -> None:
    # Given a Err(Exception()) from delete_participant
    hackathon_service_mock.delete_participant.return_value = Err(Exception())

    # When we call the handler
    resp = await hackathon_handlers.delete_participant(mock_obj_id)

    # Then the delete_participant should have been awaited once with the expected object_id
    hackathon_service_mock.delete_participant.assert_awaited_once_with(mock_obj_id)

    # And the response is a 500 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_delete_team_success(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: HackathonServiceMock,
    mock_obj_id: str,
) -> None:
    # Given an OK result from delete_team
    # Deleting a verified team has no difference from deleting an unverified team
    hackathon_service_mock.delete_team.return_value = Ok(
        Team(id=mock_obj_id, name=TEST_TEAM_NAME, is_verified=True),
    )

    # When we call the handler
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then the delete_team should have been awaited once with the expected object_id
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)

    # And the response is a 200 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TeamDeletedResponse)
    assert resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.response_model.team.id == mock_obj_id
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_team_does_not_exist(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: HackathonServiceMock,
    mock_obj_id: str,
) -> None:
    # Given a TeamNotFoundError from delete_team
    hackathon_service_mock.delete_team.return_value = Err(TeamNotFoundError())

    # When we call the handler
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then the delete_team should have been awaited once with the expected object_id
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)

    # And the response is a 404 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_team_general_exception(
    hackathon_handlers: HackathonManagementHandlers,
    hackathon_service_mock: HackathonServiceMock,
    mock_obj_id: str,
) -> None:
    # Given a Err(Exception()) from delete_team
    hackathon_service_mock.delete_team.return_value = Err(Exception())

    # When we call the handler
    resp = await hackathon_handlers.delete_team(mock_obj_id)

    # Then the delete_team should have been awaited once with the expected object_id
    hackathon_service_mock.delete_team.assert_awaited_once_with(mock_obj_id)

    # And the response is a 500 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
