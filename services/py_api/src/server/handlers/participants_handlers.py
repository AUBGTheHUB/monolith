from typing import Tuple, Type

from result import is_err, Err, Ok
from starlette import status
from starlette.responses import Response

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import DuplicateEmail, DuplicateTeamName
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import AdminParticipantRegisteredResponse, ErrResponse
from src.service.participants_service import ParticipantService


class ParticipantHandlers:
    def __init__(self, service: ParticipantService) -> None:
        self._service = service

    async def create_participant(
        self, response: Response, input_data: ParticipantRequestBody
    ) -> AdminParticipantRegisteredResponse | ErrResponse:
        result: (
            Ok[Tuple[Participant, Team]] | Err[Type[DuplicateEmail]] | Err[Type[DuplicateTeamName]] | Err[Exception]
        ) = await self._service.register_admin_participant(input_data)

        if is_err(result):
            if isinstance(result.value, DuplicateEmail):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Participant with this email already exists")

            if isinstance(result.value, DuplicateTeamName):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Team with this name already exists")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the creation of Participant")

        return AdminParticipantRegisteredResponse(participant=result.value[0], team=result.value[1])
