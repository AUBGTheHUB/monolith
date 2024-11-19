from result import is_err
from starlette import status
from starlette.responses import Response

from src.server.exception import DuplicateEmailError, DuplicateTeamNameError, HackathonCapacityExceededError
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import ParticipantRegisteredInTeamResponse, ErrResponse
from src.service.participants_service import ParticipantService
from src.server.exception import DuplicateEmailError, DuplicateTeamNameError, HackathonCapacityExceededError


class ParticipantHandlers:
    def __init__(self, service: ParticipantService) -> None:
        self._service = service

    async def create_participant(
        self, response: Response, input_data: ParticipantRequestBody
    ) -> ParticipantRegisteredInTeamResponse | ErrResponse:
        # TODO:
        # When the logic for all cases is done
        # if input_data.is_admin and input_data.team_name:
        #     result = await self._service.register_admin_participant(input_data)
        # else:
        #     ...
        if input_data.is_admin:
            result = await self._service.register_admin_participant(input_data)
        elif input_data.team_name:
            result = await self._service.register_admin_participant(input_data) #Should be changed to a function for adding a non-admin to existing team
        else:
            result = await self._service.register_random_participant(input_data)

        if is_err(result):
            # https://fastapi.tiangolo.com/advanced/response-change-status-code/
            if isinstance(result.err_value, DuplicateEmailError):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Participant with this email already exists")

            if isinstance(result.err_value, DuplicateTeamNameError):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Team with this name already exists")

            if isinstance(result.err_value, HackathonCapacityExceededError):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Max hackathon capacity has been reached")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the creation of Participant")

        return ParticipantRegisteredInTeamResponse(participant=result.ok_value[0], team=result.ok_value[1])