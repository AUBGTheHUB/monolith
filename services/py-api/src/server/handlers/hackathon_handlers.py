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

from src.server.exception import ParticipantNotFoundError, TeamNotFoundError
from src.server.schemas.response_schemas.schemas import (
    ErrResponse,
    ParticipantDeletedResponse,
    TeamDeletedResponse,
    Response,
)
from src.service.hackathon_service import HackathonService


class HackathonManagementHandlers:

    def __init__(self, service: HackathonService) -> None:
        self._service = service

    async def delete_team(self, team_id: str) -> Response:

        result = await self._service.delete_team(team_id)

        if is_err(result):
            if isinstance(result.err_value, TeamNotFoundError):
                return Response(
                    ErrResponse(error="Could not find the team with the specified id"),
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                ErrResponse(error="An unexpected error occurred during the deletion of Participant"),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(TeamDeletedResponse(team=result.ok_value), status_code=status.HTTP_200_OK)

    async def delete_participant(self, participant_id: str) -> Response:

        result = await self._service.delete_participant(participant_id)

        if is_err(result):
            if isinstance(result.err_value, ParticipantNotFoundError):
                return Response(
                    ErrResponse(error="Could not find the participant with the specified id"),
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                ErrResponse(error="An unexpected error occurred during the deletion of Participant"),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(ParticipantDeletedResponse(participant=result.ok_value), status_code=status.HTTP_200_OK)
