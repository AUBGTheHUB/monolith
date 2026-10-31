from typing import Optional
from result import Result, Ok, Err, is_err
from pymongo.asynchronous.client_session import AsyncClientSession
from src.database.model.tournament_registration.tournament_team_model import TournamentTeam
from src.database.model.tournament_registration.tournament_participant_model import TournamentParticipant

from src.exception import (
    DuplicateRegisterTournamentTeamError,
    DuplicateTournamentParticipantError,
    DuplicateTournamentTeamNameError,
    TournamentTeamFullError,
    TournamentTeamNotFoundError,
)
from src.server.schemas.request_schemas.tournament.schemas import TournamentParticipantReqData

from src.database.repository.tournament.tournament_teams_repository import TournamentTeamsRepository
from src.database.repository.tournament.tournament_participants_repository import TournamentParticipantsRepository
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.service.tournament.constants import MAX_CAPACITY
from src.service.tournament.tournament_code_service import TournamentCodeService


class TournamentRegistrationService:
    def __init__(
        self,
        tournament_teams_repo: TournamentTeamsRepository,
        tournament_participant_repo: TournamentParticipantsRepository,
        tx_manager: MongoTransactionManager,
        tournament_code_service: TournamentCodeService,
    ):
        self._tournament_teams_repo = tournament_teams_repo
        self._tournament_participant_repo = tournament_participant_repo
        self._tx_manager = tx_manager
        self._tournament_code_service = tournament_code_service

    async def register_team_member(
        self, tournament_participant: TournamentParticipantReqData, team_code: str
    ) -> Result[
        tuple[TournamentTeam, TournamentParticipant, int],
        TournamentTeamFullError | TournamentTeamNotFoundError | DuplicateTournamentParticipantError | Exception,
    ]:
        # check if participant exists
        tournament_participant_result = await self._tournament_participant_repo.find_by_email(
            email=tournament_participant.email
        )

        if is_err(tournament_participant_result):
            return tournament_participant_result

        tour_participant = tournament_participant_result.ok_value

        if tour_participant is not None:
            return Err(DuplicateTournamentParticipantError())

        # check if team exists by team code
        tournament_team_result = await self._tournament_teams_repo.find_by_code(code=team_code)

        if is_err(tournament_team_result):
            return tournament_team_result

        tournament_team = tournament_team_result.ok_value

        if tournament_team is None:
            return Err(TournamentTeamNotFoundError())

        # check member count in team
        team_members_count_result = await self._tournament_participant_repo.check_team_members_count_by_team_id(
            team_id=tournament_team.id
        )

        if is_err(team_members_count_result):
            return team_members_count_result

        if team_members_count_result.ok_value == MAX_CAPACITY:
            return Err(TournamentTeamFullError())

        tournament_team_member_result = await self._tournament_participant_repo.create(
            TournamentParticipant(
                **tournament_participant.model_dump(),
                team_id=tournament_team.id,
                is_confirmed=False,
                is_team_leader=False,
                assigned_role=tournament_participant.primary_role,
            )
        )

        if is_err(tournament_team_member_result):
            return tournament_team_member_result

        return Ok((tournament_team, tournament_team_member_result.ok_value, team_members_count_result.ok_value + 1))

    async def register_team_admin_with_transaction(
        self,
        tournament_participant: TournamentParticipantReqData,
        team_name: str,
    ) -> Result[
        tuple[TournamentTeam, TournamentParticipant],
        DuplicateRegisterTournamentTeamError
        | DuplicateTournamentTeamNameError
        | DuplicateTournamentParticipantError
        | Exception,
    ]:

        # check whether participant exists
        tournament_participant_result = await self._tournament_participant_repo.find_by_email(
            email=tournament_participant.email
        )

        if is_err(tournament_participant_result):
            return tournament_participant_result

        tour_participant = tournament_participant_result.ok_value

        if tour_participant is not None:
            return Err(DuplicateRegisterTournamentTeamError())

        team_code = self._tournament_code_service.generate_team_code()

        return await self._tx_manager.with_transaction(
            self._create_tournament_admin_and_team_in_transaction_callback,
            tour_participant=tournament_participant,
            team_code=team_code,
            team_name=team_name,
        )

    async def _create_tournament_admin_and_team_in_transaction_callback(
        self,
        tour_participant: TournamentParticipantReqData,
        team_code: str,
        team_name: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[
        tuple[TournamentTeam, TournamentParticipant],
        DuplicateTournamentTeamNameError | DuplicateTournamentParticipantError | Exception,
    ]:
        """
        This method is intended to be passed as the `callback` argument to the `TransactionManager.with_transaction(...)`
        function.
        """
        # create team first
        tournament_team = await self._tournament_teams_repo.create(
            TournamentTeam(name=team_name, code=team_code), session
        )

        if is_err(tournament_team):
            return tournament_team

        # create the tournament participant
        tournament_participant = await self._tournament_participant_repo.create(
            TournamentParticipant(
                **tour_participant.model_dump(),
                team_id=tournament_team.ok_value.id,
                is_confirmed=False,
                is_team_leader=True,
                assigned_role=tour_participant.primary_role,
            ),
            session,
        )

        if is_err(tournament_participant):
            return tournament_participant

        return Ok((tournament_team.ok_value, tournament_participant.ok_value))

    async def register_solo_member(
        self, tour_participant: TournamentParticipantReqData
    ) -> Result[TournamentParticipant, DuplicateTournamentParticipantError | Exception]:
        tournament_participant_result = await self._tournament_participant_repo.find_by_email(
            email=tour_participant.email
        )

        if is_err(tournament_participant_result):
            return tournament_participant_result

        tournament_participant = tournament_participant_result.ok_value

        if tournament_participant is not None:
            return Err(DuplicateTournamentParticipantError())

        result = await self._tournament_participant_repo.create(
            TournamentParticipant(
                **tour_participant.model_dump(),
                is_confirmed=False,
            )
        )

        if is_err(result):
            return result

        return Ok(result.ok_value)
