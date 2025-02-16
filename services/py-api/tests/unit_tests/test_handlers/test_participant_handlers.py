from unittest.mock import Mock, patch

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
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME


@pytest.fixture
def participant_handlers(participant_registration_service_mock: Mock) -> ParticipantHandlers:
    return ParticipantHandlers(participant_registration_service_mock)


@patch.dict("os.environ", {"RESEND_API_KEY": "res_some_api_key"})
@pytest.mark.asyncio
async def test_create_participant_admin_case_success(
    participant_handlers: ParticipantHandlers,
    participant_registration_service_mock: Mock,
    background_tasks: BackgroundTasks,
    mock_admin_participant: Participant,
    mock_unverified_team: Team,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Mock successful result from `register_admin_participant`
    participant_registration_service_mock.register_admin_participant.return_value = Ok(
        (
            mock_admin_participant,
            mock_unverified_team,
        )
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_admin_case, background_tasks)

    # Check that `register_admin_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Mock `register_admin_participant` to return an `Err` with `DuplicateEmailError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateEmailError(str(mock_admin_case_input_data.email))
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_admin_case, background_tasks)

    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Mock `register_admin_participant` to return an `Err` with `DuplicateTeamNameError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        DuplicateTeamNameError(mock_admin_case_input_data.team_name)
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_admin_case, background_tasks)

    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Mock `register_admin_participant` to return a general `Err`
    participant_registration_service_mock.register_admin_participant.return_value = Err(Exception("General error"))

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_admin_case, background_tasks)

    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_admin_case_input_data: AdminParticipantInputData,
    mock_participant_request_body_admin_case: ParticipantRequestBody,
) -> None:
    # Mock `register_admin_participant` to return an `Err` with `CapacityExceededError`
    participant_registration_service_mock.register_admin_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_admin_case, background_tasks)

    # Check that `register_admin_participant` was awaited once
    participant_registration_service_mock.register_admin_participant.assert_awaited_once_with(
        mock_admin_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_random_participant: Participant,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:

    # Mock the result from `register_random_participant`
    participant_registration_service_mock.register_random_participant.return_value = Ok(
        (
            mock_random_participant,
            None,
        )
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_random_case, background_tasks)

    # Check that `register_random_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Mock `register_random_participant` to return an `Err` with `DuplicateEmailError`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        DuplicateEmailError(mock_random_case_input_data.email)
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_random_case, background_tasks)

    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Mock `register_random_participant` to return a general `Err`
    participant_registration_service_mock.register_random_participant.return_value = Err(Exception("General error"))

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_random_case, background_tasks)

    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_random_case_input_data: RandomParticipantInputData,
    mock_participant_request_body_random_case: ParticipantRequestBody,
) -> None:
    # Mock `register_random_participant` to return an `Err` with `CapacityExceededError`
    participant_registration_service_mock.register_random_participant.return_value = Err(
        HackathonCapacityExceededError()
    )

    # Call the handler
    resp = await participant_handlers.create_participant(mock_participant_request_body_random_case, background_tasks)

    # Check that `register_random_participant` was awaited once
    participant_registration_service_mock.register_random_participant.assert_awaited_once_with(
        mock_random_case_input_data, background_tasks
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
    background_tasks: BackgroundTasks,
    mock_invite_participant: Participant,
    mock_verified_team: Team,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
    mock_obj_id: str,
) -> None:
    # Mock successful result from `register_invite_link_participant`
    participant_registration_service_mock.register_invite_link_participant.return_value = Ok(
        (
            mock_invite_participant,
            mock_verified_team,
        )
    )

    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks, "mock_jwt_token"
    )

    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks
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
    background_tasks: BackgroundTasks,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        DuplicateEmailError(str(mock_invite_link_case_input_data.email))
    )

    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks, "mock_jwt_token"
    )

    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks
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
    background_tasks: BackgroundTasks,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        Exception("General error")
    )

    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks, "mock_jwt_token"
    )

    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks
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
    background_tasks: BackgroundTasks,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(
        TeamCapacityExceededError()
    )

    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks, "mock_jwt_token"
    )

    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks
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
    background_tasks: BackgroundTasks,
    mock_invite_link_case_input_data: InviteLinkParticipantInputData,
    mock_participant_request_body_invite_link_case: ParticipantRequestBody,
) -> None:
    participant_registration_service_mock.register_invite_link_participant.return_value = Err(TeamNotFoundError())

    # Call the handler
    resp = await participant_handlers.create_participant(
        mock_participant_request_body_invite_link_case, background_tasks, "mock_jwt_token"
    )

    # Check that `register_invite_link_participant` was awaited once with the expected input_data
    participant_registration_service_mock.register_invite_link_participant.assert_awaited_once_with(
        mock_invite_link_case_input_data, "mock_jwt_token", background_tasks
    )

    # Assert the response indicates a conflict
    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.response_model.error == "The specified team was not found"
    resp.status_code = status.HTTP_404_NOT_FOUND
