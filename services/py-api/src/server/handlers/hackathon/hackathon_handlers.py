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
from src.server.schemas.response_schemas.hackathon.schemas import (
    AllParticipantsResponse,
    ParticipantDeletedResponse,
    TeamDeletedResponse,
    AllTeamsResponse,
)
from src.server.schemas.response_schemas.schemas import Response, FeatureSwitchResponse
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.team_service import TeamService


class HackathonManagementHandlers(BaseHandler):

    def __init__(
        self,
        hackathon_utility_service: HackathonUtilityService,
        participant_service: ParticipantService,
        team_service: TeamService,
    ) -> None:
        self._hackathon_utility_service = hackathon_utility_service
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

    async def get_all_participants(self) -> Response:
        participants_result = await self._participant_service.fetch_all_participants()
        if is_err(participants_result):
            return self.handle_error(participants_result.err_value)

        teams_result = await self._team_service.fetch_all_teams()
        if is_err(teams_result):
            return self.handle_error(teams_result.err_value)
        # Build a team_id -> team_name lookup so we can display team names instead of raw ObjectIds
        team_names = {str(team.id): team.name for team in teams_result.ok_value}

        participants_data = []
        for participant in participants_result.ok_value:
            data = participant.dump_as_json()
            data["team_name"] = team_names.get(data["team_id"]) if data.get("team_id") else None
            participants_data.append(data)

        return Response(
            AllParticipantsResponse(participants=participants_data),
            status_code=status.HTTP_200_OK,
        )

    async def delete_participant(self, object_id: str) -> Response:
        result = await self._participant_service.delete_participant(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(ParticipantDeletedResponse(participant=result.ok_value), status_code=status.HTTP_200_OK)

    async def close_registration(self) -> Response:

        result = await self._hackathon_utility_service.close_reg_for_all_participants()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(FeatureSwitchResponse(feature=result.ok_value), status_code=status.HTTP_200_OK)
