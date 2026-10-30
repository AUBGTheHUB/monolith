from result import is_err
from fastapi import BackgroundTasks

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.tournament.schemas import (
    TournamentAdminTeamReqData,
    TournamentParticipantJoinTeamReqData,
    TournamentParticipantReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.tournament.constants import MAX_CAPACITY

from src.server.schemas.response_schemas.tournament.schemas import (
    TournamentSoloParticipantResponse,
    TournamentTeamAndParticipantResponse,
)
from src.service.tournament.tournament_services import TournamentRegistrationService

from src.service.tournament.tournament_mail_service import TournamentMailService


class TournamentRegistrationHandlers(BaseHandler):
    def __init__(
        self, tournament_service: TournamentRegistrationService, tournament_mail_service: TournamentMailService
    ) -> None:
        self._tournament_service = tournament_service
        self._tournament_mail_service = tournament_mail_service

    async def register_team_and_admin_handler(
        self, data: TournamentAdminTeamReqData, background_tasks: BackgroundTasks
    ) -> Response:
        result = await self._tournament_service.register_team_admin_with_transaction(
            tournament_participant=data.tournament_participant, team_name=data.team_name
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        email_result = await self._tournament_mail_service.send_email_with_team_code(
            tournament_participant=result.ok_value[1],
            team_code=result.ok_value[0].code,
            background_tasks=background_tasks,
        )

        if is_err(email_result):
            return self.handle_error(email_result.err_value)

        return Response(
            response_model=TournamentTeamAndParticipantResponse(
                tournament_team=result.ok_value[0], tournament_participant=result.ok_value[1]
            ),
            status_code=201,
        )

    async def register_team_member_handler(
        self, data: TournamentParticipantJoinTeamReqData, background_tasks: BackgroundTasks
    ) -> Response:
        result = await self._tournament_service.register_team_member(
            tournament_participant=data.tournament_participant, team_code=data.team_code
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        tournament_team = result.ok_value[0]
        tournament_participant = result.ok_value[1]

        # TODO
        if result.ok_value[2] == MAX_CAPACITY:
            email_result = await self._tournament_mail_service.send_email_when_team_is_complete(
                tournament_participant=result.ok_value[1],
                team_name=tournament_team.name,
                background_tasks=background_tasks,
            )

            if is_err(email_result):
                return self.handle_error(email_result.err_value)

        return Response(
            response_model=TournamentTeamAndParticipantResponse(
                tournament_team=tournament_team, tournament_participant=tournament_participant
            ),
            status_code=201,
        )

    async def register_solo_handler(
        self,
        data: TournamentParticipantReqData,
    ) -> Response:

        result = await self._tournament_service.register_solo_member(tour_participant=data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=TournamentSoloParticipantResponse(tournament_participant=result.ok_value), status_code=201
        )
