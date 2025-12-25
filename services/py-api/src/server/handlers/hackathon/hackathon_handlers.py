# The HTTP handlers defined here are responsible for accepting requests passed from the routes, and returning responses
# in JSON format. This separation is done in order to improve testability and modularity.
#
# To return a custom type-safe JSON response we recommend using the server.schemas.response_schemas.Response object. By
# doing so you will be returning ResponseModels (aka ResponseSchemas in OpenAPI spec terms), and adhering to the
# OpenAPI spec defined in the routes via `responses` or `response_model` arguments.
#
# For more info: https://fastapi.tiangolo.com/advanced/additional-responses/

from result import is_err
from starlette import status

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import (
    ParticipantDeletedResponse,
    TeamDeletedResponse,
    Response,
    AllTeamsResponse,
    FeatureSwitchResponse,
)
from src.service.hackathon.hackathon_service import HackathonService
from src.service.hackathon.participants.participant_service import ParticipantService
from src.service.hackathon.teams.team_service import TeamService


class HackathonManagementHandlers(BaseHandler):

    def __init__(
        self, hackathon_service: HackathonService, participant_service: ParticipantService, team_service: TeamService
    ) -> None:
        self._hackathon_service = hackathon_service
        self._participant_service = participant_service
        self._team_service = team_service

    async def delete_team(self, object_id: str) -> Response:
        result = await self._team_service.delete_team(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(TeamDeletedResponse(team=result.ok_value), status_code=status.HTTP_200_OK)

    async def get_all_teams(self) -> Response:
        result = await self._team_service.fetch_all_teams()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(AllTeamsResponse(teams=result.ok_value), status_code=status.HTTP_200_OK)

    async def delete_participant(self, object_id: str) -> Response:
        result = await self._participant_service.delete_participant(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(ParticipantDeletedResponse(participant=result.ok_value), status_code=status.HTTP_200_OK)

    async def close_registration(self) -> Response:

        result = await self._hackathon_service.close_reg_for_all_participants()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(FeatureSwitchResponse(feature=result.ok_value), status_code=status.HTTP_200_OK)
