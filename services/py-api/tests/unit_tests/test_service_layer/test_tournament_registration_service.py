from typing import cast

import pytest
from result import Ok, Err

from src.database.model.tournament_registration.tournament_participant_model import TournamentParticipant
from src.database.model.tournament_registration.tournament_team_model import TournamentTeam
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.tournament.tournament_participants_repository import TournamentParticipantsRepository
from src.database.repository.tournament.tournament_teams_repository import TournamentTeamsRepository
from src.exception import (
    DuplicateTournamentParticipantError,
    TournamentTeamNotFoundError,
    TournamentTeamFullError,
    DuplicateRegisterTournamentTeamError,
    DuplicateTournamentTeamNameError,
)
from src.server.schemas.request_schemas.tournament.schemas import TournamentParticipantReqData
from src.service.tournament.constants import MAX_CAPACITY
from src.service.tournament.tournament_code_service import TournamentCodeService
from src.service.tournament.tournament_registration_service import TournamentRegistrationService
from tests.unit_tests.conftest import (
    TournamentParticipantsRepoMock,
    TournamentCodeServiceMock,
    MongoTransactionManagerMock,
    TournamentTeamsRepoMock,
)


@pytest.fixture
def tournament_service(
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
    tournament_code_service_mock: TournamentCodeServiceMock,
) -> TournamentRegistrationService:
    return TournamentRegistrationService(
        cast(TournamentTeamsRepository, tournament_teams_repo_mock),
        cast(TournamentParticipantsRepository, tournament_participants_repo_mock),
        cast(MongoTransactionManager, tx_manager_mock),
        cast(TournamentCodeService, tournament_code_service_mock),
    )


@pytest.mark.asyncio
async def test_register_team_member_success(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_team_mock: TournamentTeam,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    current_members = MAX_CAPACITY - 1
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.return_value = Ok(current_members)
    tournament_participants_repo_mock.create.return_value = Ok(tournament_participant_mock)

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result.is_ok()
    assert result.ok_value == (tournament_team_mock, tournament_participant_mock, current_members + 1)

    tournament_participants_repo_mock.find_by_email.assert_awaited_once_with(
        email=tournament_solo_participant_req_data.email
    )
    tournament_teams_repo_mock.find_by_code.assert_awaited_once_with(code=tournament_team_code_mock)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.assert_awaited_once_with(
        team_id=tournament_team_mock.id
    )

    created = tournament_participants_repo_mock.create.call_args.args[0]
    assert created.team_id == tournament_team_mock.id
    assert created.email == tournament_solo_participant_req_data.email
    assert created.is_team_leader is False
    assert created.is_confirmed is False


@pytest.mark.asyncio
async def test_register_team_member_duplicate_participant(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(tournament_participant_mock)

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result.is_err()
    assert isinstance(result.err_value, DuplicateTournamentParticipantError)
    tournament_teams_repo_mock.find_by_code.assert_not_awaited()
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_find_by_email_error(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = error

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result is error
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_team_not_found(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = Ok(None)

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result.is_err()
    assert isinstance(result.err_value, TournamentTeamNotFoundError)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.assert_not_awaited()
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_find_by_code_error(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = error

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result is error
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_team_full(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_team_mock: TournamentTeam,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.return_value = Ok(MAX_CAPACITY)

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result.is_err()
    assert isinstance(result.err_value, TournamentTeamFullError)
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_count_error(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_team_mock: TournamentTeam,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.return_value = error

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result is error
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_member_create_error(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_team_mock: TournamentTeam,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_code_mock: str,
) -> None:
    error = Err(DuplicateTournamentParticipantError())
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_teams_repo_mock.find_by_code.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.check_team_members_count_by_team_id.return_value = Ok(1)
    tournament_participants_repo_mock.create.return_value = error

    result = await tournament_service.register_team_member(
        tournament_solo_participant_req_data, tournament_team_code_mock
    )

    assert result is error


@pytest.mark.asyncio
async def test_register_team_admin_with_transaction_success(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_code_service_mock: TournamentCodeServiceMock,
    tx_manager_mock: MongoTransactionManagerMock,
    tournament_team_mock: TournamentTeam,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
    tournament_team_code_mock: str,
) -> None:
    expected = Ok((tournament_team_mock, tournament_participant_mock))
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_code_service_mock.generate_team_code.return_value = tournament_team_code_mock
    tx_manager_mock.with_transaction.return_value = expected

    result = await tournament_service.register_team_admin_with_transaction(
        tournament_solo_participant_req_data, tournament_team_name_mock
    )

    assert result is expected
    tournament_code_service_mock.generate_team_code.assert_called_once()
    tx_manager_mock.with_transaction.assert_awaited_once_with(
        tournament_service._create_tournament_admin_and_team_in_transaction_callback,
        tour_participant=tournament_solo_participant_req_data,
        team_code=tournament_team_code_mock,
        team_name=tournament_team_name_mock,
    )


@pytest.mark.asyncio
async def test_register_team_admin_with_transaction_duplicate_participant(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_code_service_mock: TournamentCodeServiceMock,
    tx_manager_mock: MongoTransactionManagerMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(tournament_participant_mock)

    result = await tournament_service.register_team_admin_with_transaction(
        tournament_solo_participant_req_data, tournament_team_name_mock
    )

    assert result.is_err()
    assert isinstance(result.err_value, DuplicateRegisterTournamentTeamError)
    tournament_code_service_mock.generate_team_code.assert_not_called()
    tx_manager_mock.with_transaction.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_team_admin_with_transaction_find_by_email_error(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tx_manager_mock: MongoTransactionManagerMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = error

    result = await tournament_service.register_team_admin_with_transaction(
        tournament_solo_participant_req_data, tournament_team_name_mock
    )

    assert result is error
    tx_manager_mock.with_transaction.assert_not_awaited()


@pytest.mark.asyncio
async def test_transaction_callback_success(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_team_mock: TournamentTeam,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
    tournament_team_code_mock: str,
) -> None:
    tournament_teams_repo_mock.create.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.create.return_value = Ok(tournament_participant_mock)

    result = await tournament_service._create_tournament_admin_and_team_in_transaction_callback(
        tour_participant=tournament_solo_participant_req_data,
        team_code=tournament_team_code_mock,
        team_name=tournament_team_name_mock,
    )

    assert result.is_ok()
    assert result.ok_value == (tournament_team_mock, tournament_participant_mock)

    team = tournament_teams_repo_mock.create.call_args.args[0]
    assert team.name == tournament_team_name_mock
    assert team.code == tournament_team_code_mock

    participant = tournament_participants_repo_mock.create.call_args.args[0]
    assert participant.team_id == tournament_team_mock.id
    assert participant.is_team_leader is True
    assert participant.is_confirmed is False


@pytest.mark.asyncio
async def test_transaction_callback_team_creation_fails(
    tournament_service: TournamentRegistrationService,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
    tournament_team_code_mock: str,
) -> None:
    error = Err(DuplicateTournamentTeamNameError())
    tournament_teams_repo_mock.create.return_value = error

    result = await tournament_service._create_tournament_admin_and_team_in_transaction_callback(
        tour_participant=tournament_solo_participant_req_data,
        team_code=tournament_team_code_mock,
        team_name=tournament_team_name_mock,
    )

    assert result is error
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_transaction_callback_participant_creation_fails(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_teams_repo_mock: TournamentTeamsRepoMock,
    tournament_team_mock: TournamentTeam,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
    tournament_team_name_mock: str,
    tournament_team_code_mock: str,
) -> None:
    error = Err(DuplicateTournamentParticipantError())
    tournament_teams_repo_mock.create.return_value = Ok(tournament_team_mock)
    tournament_participants_repo_mock.create.return_value = error

    result = await tournament_service._create_tournament_admin_and_team_in_transaction_callback(
        tour_participant=tournament_solo_participant_req_data,
        team_code=tournament_team_code_mock,
        team_name=tournament_team_name_mock,
    )

    assert result is error


@pytest.mark.asyncio
async def test_register_solo_member_success(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_participants_repo_mock.create.return_value = Ok(tournament_participant_mock)

    result = await tournament_service.register_solo_member(tournament_solo_participant_req_data)

    assert result.is_ok()
    assert result.ok_value == tournament_participant_mock
    tournament_participants_repo_mock.find_by_email.assert_awaited_once_with(
        email=tournament_solo_participant_req_data.email
    )
    created = tournament_participants_repo_mock.create.call_args.args[0]
    assert created.email == tournament_solo_participant_req_data.email
    assert created.is_confirmed is False


@pytest.mark.asyncio
async def test_register_solo_member_duplicate(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_participant_mock: TournamentParticipant,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
) -> None:
    tournament_participants_repo_mock.find_by_email.return_value = Ok(tournament_participant_mock)

    result = await tournament_service.register_solo_member(tournament_solo_participant_req_data)

    assert result.is_err()
    assert isinstance(result.err_value, DuplicateTournamentParticipantError)
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_solo_member_find_by_email_error(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = error

    result = await tournament_service.register_solo_member(tournament_solo_participant_req_data)

    assert result is error
    tournament_participants_repo_mock.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_solo_member_create_error(
    tournament_service: TournamentRegistrationService,
    tournament_participants_repo_mock: TournamentParticipantsRepoMock,
    tournament_solo_participant_req_data: TournamentParticipantReqData,
) -> None:
    error = Err(Exception("Fake Error"))
    tournament_participants_repo_mock.find_by_email.return_value = Ok(None)
    tournament_participants_repo_mock.create.return_value = error

    result = await tournament_service.register_solo_member(tournament_solo_participant_req_data)

    assert result is error
