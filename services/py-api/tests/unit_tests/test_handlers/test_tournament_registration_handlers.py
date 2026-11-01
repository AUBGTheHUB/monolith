from __future__ import annotations

import pytest
from typing import cast
from result import Err, Ok

from src.database.model.tournament_registration.tournament_participant_model import TournamentParticipant
from src.database.model.tournament_registration.tournament_team_model import TournamentTeam
from src.exception import DuplicateTournamentParticipantError, DuplicateTournamentTeamNameError
from src.server.handlers.tournament.tournament_registration_handlers import TournamentRegistrationHandlers
from src.server.schemas.request_schemas.tournament.schemas import (
    TournamentAdminTeamReqData,
    TournamentParticipantJoinTeamReqData,
    TournamentParticipantReqData,
)
from src.server.schemas.response_schemas.schemas import ErrResponse, Response
from src.server.schemas.response_schemas.tournament.schemas import (
    TournamentSoloParticipantResponse,
    TournamentTeamAndParticipantResponse,
)
from src.service.tournament.tournament_mail_service import TournamentMailService
from src.service.tournament.tournament_registration_service import TournamentRegistrationService

from tests.unit_tests.conftest import BackgroundTasksMock, TournamentMailServiceMock, TournamentRegistrationServiceMock


@pytest.fixture
def tournament_registration_handlers(
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_mail_service_mock: TournamentMailServiceMock,
) -> TournamentRegistrationHandlers:
    return TournamentRegistrationHandlers(
        cast(TournamentRegistrationService, tournament_registration_service_mock),
        cast(TournamentMailService, tournament_mail_service_mock),
    )


@pytest.mark.asyncio
async def test_register_team_admin_and_team_returns_201(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_mail_service_mock: TournamentMailServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    tournament_team_mock: TournamentTeam,
    tournament_participant_mock: TournamentParticipant,
    tournament_admin_participant_with_team_req_data: TournamentAdminTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_admin_with_transaction.return_value = Ok(
        (tournament_team_mock, tournament_participant_mock)
    )
    tournament_mail_service_mock.send_email_with_team_code.return_value = Ok(None)

    resp = await tournament_registration_handlers.register_team_and_admin_handler(
        data=tournament_admin_participant_with_team_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    assert isinstance(resp.response_model, TournamentTeamAndParticipantResponse)
    tournament_registration_service_mock.register_team_admin_with_transaction.assert_awaited_once()
    tournament_mail_service_mock.send_email_with_team_code.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_admin_and_team_returns_409_when_registering_with_existing_email(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    tournament_admin_participant_with_team_req_data: TournamentAdminTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_admin_with_transaction.return_value = Err(
        DuplicateTournamentParticipantError()
    )
    resp = await tournament_registration_handlers.register_team_and_admin_handler(
        data=tournament_admin_participant_with_team_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == 409
    assert resp.response_model.error == "Tournament participant with this email already exists"
    tournament_registration_service_mock.register_team_admin_with_transaction.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_admin_and_team_returns_409_when_registering_with_existing_team_name(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    tournament_admin_participant_with_team_req_data: TournamentAdminTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_admin_with_transaction.return_value = Err(
        DuplicateTournamentTeamNameError()
    )
    resp = await tournament_registration_handlers.register_team_and_admin_handler(
        data=tournament_admin_participant_with_team_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == 409
    assert resp.response_model.error == "Tournament team with this team already exists"
    tournament_registration_service_mock.register_team_admin_with_transaction.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_member_handler_returns_201(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_team_mock: TournamentTeam,
    tournament_participant_mock: TournamentParticipant,
    background_tasks_mock: BackgroundTasksMock,
    tournament_participant_with_code_req_data: TournamentParticipantJoinTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_member.return_value = Ok(
        (tournament_team_mock, tournament_participant_mock, 2)
    )

    resp = await tournament_registration_handlers.register_team_member_handler(
        data=tournament_participant_with_code_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TournamentTeamAndParticipantResponse)
    assert resp.status_code == 201
    tournament_registration_service_mock.register_team_member.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_member_handler_returns_201_and_sends_email_when_5_people_have_registered(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_mail_service_mock: TournamentMailServiceMock,
    tournament_team_mock: TournamentTeam,
    tournament_participant_mock: TournamentParticipant,
    background_tasks_mock: BackgroundTasksMock,
    tournament_participant_with_code_req_data: TournamentParticipantJoinTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_member.return_value = Ok(
        (tournament_team_mock, tournament_participant_mock, 5)
    )
    tournament_mail_service_mock.send_email_when_team_is_complete.return_value = Ok(None)

    resp = await tournament_registration_handlers.register_team_member_handler(
        data=tournament_participant_with_code_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TournamentTeamAndParticipantResponse)
    assert resp.status_code == 201
    tournament_registration_service_mock.register_team_member.assert_awaited_once()
    tournament_mail_service_mock.send_email_when_team_is_complete.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_member_returns_409_when_registering_with_existing_email(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    tournament_participant_with_code_req_data: TournamentParticipantJoinTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_member.return_value = Err(DuplicateTournamentParticipantError())
    resp = await tournament_registration_handlers.register_team_member_handler(
        data=tournament_participant_with_code_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == 409
    assert resp.response_model.error == "Tournament participant with this email already exists"
    tournament_registration_service_mock.register_team_member.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_team_member_returns_409_when_registering_with_existing_team_name(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    background_tasks_mock: BackgroundTasksMock,
    tournament_participant_with_code_req_data: TournamentParticipantJoinTeamReqData,
) -> None:

    tournament_registration_service_mock.register_team_member.return_value = Err(DuplicateTournamentTeamNameError())
    resp = await tournament_registration_handlers.register_team_member_handler(
        data=tournament_participant_with_code_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == 409
    assert resp.response_model.error == "Tournament team with this team already exists"
    tournament_registration_service_mock.register_team_member.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_solo_handler_returns_201(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    background_tasks_mock: BackgroundTasksMock,
) -> None:

    tournament_registration_service_mock.register_solo_member.return_value = Ok(tournament_participant_mock)

    resp = await tournament_registration_handlers.register_solo_handler(
        data=tournament_solo_participant_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, TournamentSoloParticipantResponse)
    assert resp.status_code == 201
    tournament_registration_service_mock.register_solo_member.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_solo_handler_returns_409_when_registering_with_an_existing_email(
    tournament_registration_handlers: TournamentRegistrationHandlers,
    tournament_registration_service_mock: TournamentRegistrationServiceMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    background_tasks_mock: BackgroundTasksMock,
) -> None:

    tournament_registration_service_mock.register_solo_member.return_value = Err(DuplicateTournamentParticipantError())

    resp = await tournament_registration_handlers.register_solo_handler(
        data=tournament_solo_participant_req_data,
        background_tasks=background_tasks_mock,
    )

    assert isinstance(resp, Response)
    assert isinstance(resp.response_model, ErrResponse)
    assert resp.status_code == 409
    assert resp.response_model.error == "Tournament participant with this email already exists"
    tournament_registration_service_mock.register_solo_member.assert_awaited_once()
