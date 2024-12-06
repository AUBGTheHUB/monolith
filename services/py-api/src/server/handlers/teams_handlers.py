from result import is_err
from starlette import status
from starlette.responses import Response

from src.server.exception import TeamNotFound
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse
from src.database.repository.teams_repository import TeamsRepository


class TeamHandlers:

    def __init__(self, repository: TeamsRepository) -> None:
        self._repository = repository

    async def delete_team(self, response: Response, team_id: str) -> TeamDeletedResponse | ErrResponse:

        result = await self._repository.delete(team_id)

        if is_err(result):
            if isinstance(result.err_value, TeamNotFound):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="Could not find the team with the specified id")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the deletion of Participant")

        return TeamDeletedResponse(team=result.ok_value)
