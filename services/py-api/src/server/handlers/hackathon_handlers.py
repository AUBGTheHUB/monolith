from result import is_err
from starlette import status
from starlette.responses import Response

from src.server.exception import ParticipantNotFoundError, TeamNotFoundError
from src.server.schemas.response_schemas.schemas import ErrResponse, ParticipantDeletedResponse, TeamDeletedResponse
from src.service.hackathon_service import HackathonService


class HackathonManagementHandlers:

    def __init__(self, service: HackathonService) -> None:
        self._service = service

    async def delete_team(self, response: Response, team_id: str) -> TeamDeletedResponse | ErrResponse:

        result = await self._service.delete_team(team_id)

        if is_err(result):
            if isinstance(result.err_value, TeamNotFoundError):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="Could not find the team with the specified id")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the deletion of Participant")

        return TeamDeletedResponse(team=result.ok_value)

    async def delete_participant(
        self, response: Response, participant_id: str
    ) -> ParticipantDeletedResponse | ErrResponse:

        result = await self._service.delete_participant(participant_id)

        if is_err(result):
            if isinstance(result.err_value, ParticipantNotFoundError):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="Could not find the participant with the specified id")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the deletion of Participant")

        return ParticipantDeletedResponse(participant=result.ok_value)
