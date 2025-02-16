from typing import cast

from fastapi import BackgroundTasks
import pytest
from result import Ok, Err
from starlette import status

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNotFoundError,
)
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    ParticipantRequestBody,
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.server.schemas.response_schemas.schemas import ErrResponse, Response, ParticipantRegisteredResponse
from src.service.participants_registration_service import ParticipantRegistrationService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import ParticipantRegistrationServiceMock, BackgroundTasksMock


@pytest.fixture
def participant_handlers(
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
) -> ParticipantHandlers:
    return ParticipantHandlers(service=cast(ParticipantRegistrationService, participant_registration_service_mock))


@pytest.mark.asyncio
async def test_create_participant_admin_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
    mock_admin_participant: Participant,
    mock_normal_team: Team,
) -> None:
    # Given an OK result from `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Ok(
        (mock_admin_participant, mock_normal_team)
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_admin_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # And the response is a 201 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is True
    assert resp.response_model.team is not None and resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_participant_admin_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Given a DuplicateEmailError returned by `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateEmailError(str(mock_admin_case_input_data.email))
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_admin_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_admin_case_duplicate_team_name_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Given a DuplicateTeamNameError returned by `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateTeamNameError(mock_admin_case_input_data.team_name)
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_admin_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Team with this name already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_admin_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Given an Err(Exception()) returned by `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Err(Exception("General error"))

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_admin_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # And the response is a 500 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_create_participant_admin_case_capacity_exceeded_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Given an HackathonCapacityExceededError returned by `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_admin_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_random_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
    mock_random_participant: Participant,
) -> None:
    # Given an OK result from `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Ok((mock_random_participant, None))

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_random_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # And the response is a 201 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is False
    assert resp.response_model.team is None
    resp.status_code = status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_participant_random_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Given a DuplicateEmailError from `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        DuplicateEmailError(cast(str, mock_random_case_input_data.email))
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_random_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_random_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Given an Err(Exception()) returned by `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Err(Exception("General error"))

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_random_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # And the response is a 500 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_create_participant_random_case_capacity_exceeded_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Given a CapacityExceededError returned by `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, cast(BackgroundTasks, background_tasks_mock)
    )

    # Then `register_random_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_link_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_invite_participant: Participant,
    mock_normal_team: Team,
    mock_jwt_token: str,
) -> None:
    # Given an OK result from `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Ok(
        (mock_invite_participant, mock_normal_team)
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, cast(BackgroundTasks, background_tasks_mock), mock_jwt_token
    )

    # Then `register_invite_link_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, mock_jwt_token, background_tasks_mock
    )

    # And the response is a 201 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is False
    assert resp.response_model.team is not None and resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.response_model.team.id == resp.response_model.participant.team_id
    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_participant_link_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_jwt_token: str,
) -> None:
    # Given a DuplicateEmailError returned by `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        DuplicateEmailError(str(mock_invite_link_case_input_data.email))
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, cast(BackgroundTasks, background_tasks_mock), mock_jwt_token
    )

    # Then `register_invite_link_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, mock_jwt_token, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_link_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_jwt_token: str,
) -> None:
    # Given an Err(Exception()) returned by `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        Exception("General error")
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, cast(BackgroundTasks, background_tasks_mock), mock_jwt_token
    )

    # Then `register_invite_link_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, mock_jwt_token, background_tasks_mock
    )

    # And the response is a 500 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_create_participant_link_case_team_capacity_exceeded(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_jwt_token: str,
) -> None:
    # Given a TeamCapacityExceededError returned by `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        TeamCapacityExceededError()
    )

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, cast(BackgroundTasks, background_tasks_mock), mock_jwt_token
    )

    # Then `register_invite_link_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, mock_jwt_token, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max team capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_participant_link_case_team_not_found(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_jwt_token: str,
) -> None:
    # Given a TeamNotFoundError returned by `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(TeamNotFoundError())

    # When we call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, cast(BackgroundTasks, background_tasks_mock), mock_jwt_token
    )

    # Then `register_invite_link_participant` should have been awaited once with expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, mock_jwt_token, background_tasks_mock
    )

    # And the response is a 409 one
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    resp.status_code = status.HTTP_404_NOT_FOUND
