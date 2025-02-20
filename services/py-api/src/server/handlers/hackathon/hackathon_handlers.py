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
)
from src.service.hackathon.hackathon_service import HackathonService


class HackathonManagementHandlers(BaseHandler):

    def __init__(self, service: HackathonService) -> None:
        self._service = service

    async def delete_team(self, team_id: str) -> Response:
        result = await self._service.delete_team(team_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(TeamDeletedResponse(team=result.ok_value), status_code=status.HTTP_200_OK)

    async def delete_participant(self, participant_id: str) -> Response:
        result = await self._service.delete_participant(participant_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(ParticipantDeletedResponse(participant=result.ok_value), status_code=status.HTTP_200_OK)


def hackathon_management_handlers_provider(service: HackathonService) -> HackathonManagementHandlers:
    """
    Args:
        service: A HackathonService instance

    Returns:
        A HackathonManagementHandlers instance
    """
    return HackathonManagementHandlers(service=service)
