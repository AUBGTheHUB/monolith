from result import is_err
from starlette import status
from starlette.responses import Response

from src.database.repositories.participants_repository import ParticipantsRepository
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import ParticipantResponse, ErrResponse


class ParticipantHandlers:
    def __init__(self, repository: ParticipantsRepository) -> None:
        self._repository = repository

    async def create_participant(
        self, response: Response, req_body: ParticipantRequestBody
    ) -> ParticipantResponse | ErrResponse:
        # TODO: Update statuses based on errors
        result = await self._repository.create(req_body)
        if is_err(result):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the creation of Participant")

        return result.ok_value  # type: ignore[no-any-return]
