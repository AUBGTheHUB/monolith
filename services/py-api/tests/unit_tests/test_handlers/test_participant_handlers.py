from typing import cast
from unittest.mock import Mock, patch

import pytest
from result import Ok, Err
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNotFoundError,
)
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from starlette import status

from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    ParticipantRequestBody,
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.server.schemas.response_schemas.schemas import ErrResponse, Response, ParticipantRegisteredResponse
from src.service.hackathon.participants_registration_service import ParticipantRegistrationService
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME
from tests.unit_tests.conftest import ParticipantRegistrationServiceMock, BackgroundTasksMock


@pytest.fixture
def participant_handlers(
    participant_registration_service_mock: ParticipantRegistrationServiceMock,
) -> ParticipantHandlers:
    return ParticipantHandlers(cast(ParticipantRegistrationService, participant_registration_service_mock))


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_participant: Participant,
    mock_unverified_team: Team,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock successful result from `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Ok(
        (
            mock_admin_participant,
            mock_unverified_team,
        )
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, background_tasks_mock
    )

    # Then
    # Check that `register_admin_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is True
    assert resp.response_model.team is not None and resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.status_code == status.HTTP_201_CREATED


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_admin_participant` to return an `Err` with `DuplicateEmailError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateEmailError(str(mock_admin_case_input_data.email))
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, background_tasks_mock
    )

    # Then
    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_duplicate_team_name_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_admin_participant` to return an `Err` with `DuplicateTeamNameError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateTeamNameError(mock_admin_case_input_data.team_name)
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, background_tasks_mock
    )

    # Then
    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Team with this name already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_admin_participant` to return a general `Err`
    participant_registration_service_mock.register_admin_participant.return_value = Err(Exception("General error"))

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, background_tasks_mock
    )

    # Then
    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # Assert the response indicates an internal server error
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_capacity_exceeded_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_admin_participant` to return an `Err` with `CapacityExceededError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_admin_case, background_tasks_mock
    )

    # Then
    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks_mock
    )

    # Assert the response indicates a conflict with capacity reached
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_random_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock the result from `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Ok(
        (
            mock_random_participant,
            None,
        )
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, background_tasks_mock
    )

    # Then
    # Check that `register_random_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is False
    assert resp.response_model.team is None
    resp.status_code = status.HTTP_201_CREATED


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_random_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_random_participant` to return an `Err` with `DuplicateEmailError`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        DuplicateEmailError(mock_random_case_input_data.email)
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, background_tasks_mock
    )

    # Then
    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_random_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_random_participant` to return a general `Err`
    participant_registration_service_mock.register_random_participant.return_value = Err(Exception("General error"))

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, background_tasks_mock
    )

    # Then
    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # Assert the response indicates an internal server error
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_random_case_capacity_exceeded_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:

    # Given
    # Mock `register_random_participant` to return an `Err` with `CapacityExceededError`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_random_case, background_tasks_mock
    )

    # Then
    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks_mock
    )

    # Assert the response indicates a conflict with capacity reached
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max hackathon capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_link_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_participant: Participant,
    mock_verified_team: Team,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_obj_id: str,
) -> None:

    # Given
    # Mock successful result from `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Ok(
        (
            mock_invite_participant,
            mock_verified_team,
        )
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks_mock, "mock_jwt_token"
    )

    # Then
    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks_mock
    )

    # Assert that the response is successful
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ParticipantRegisteredResponse)
    assert resp.response_model.participant.name == TEST_USER_NAME
    assert resp.response_model.participant.email == TEST_USER_EMAIL
    assert resp.response_model.participant.is_admin is False
    assert resp.response_model.team is not None and resp.response_model.team.name == TEST_TEAM_NAME
    assert resp.response_model.team.id == resp.response_model.participant.team_id
    assert resp.status_code == status.HTTP_201_CREATED


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_link_case_duplicate_email_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:

    # Given
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        DuplicateEmailError(str(mock_invite_link_case_input_data.email))
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks_mock, "mock_jwt_token"
    )

    # Then
    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Participant with this email already exists"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_link_case_general_error(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:

    # Given
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        Exception("General error")
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks_mock, "mock_jwt_token"
    )

    # Then
    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "An unexpected error occurred"
    resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_link_case_team_capacity_exceeded(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:

    # Given
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        TeamCapacityExceededError()
    )

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks_mock, "mock_jwt_token"
    )

    # Then
    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "Max team capacity has been reached"
    resp.status_code = status.HTTP_409_CONFLICT


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_link_case_team_not_found(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks_mock: BackgroundTasksMock,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:

    # Given
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(TeamNotFoundError())

    # When
    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks_mock, "mock_jwt_token"
    )

    # Then
    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks_mock
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    resp.status_code = status.HTTP_404_NOT_FOUND
