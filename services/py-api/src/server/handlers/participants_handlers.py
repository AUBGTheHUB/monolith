from result import is_err
from starlette import status
from starlette.responses import Response

from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    ParticipantNotFound,
)
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
    ParticipantDeletedResponse,
)
from src.service.participants_registration_service import ParticipantRegistrationService


class ParticipantHandlers:

    def __init__(self, service: ParticipantRegistrationService) -> None:
        self._service = service

    async def delete_participant(
        self, response: Response, participant_id: str
    ) -> ParticipantDeletedResponse | ErrResponse:

        # Direct access to the participant repository to facilitate CRUD operations
        _repository = self._service._hackathon_service._participant_repo

        result = await _repository.delete(participant_id)

        if is_err(result):
            if isinstance(result.err_value, ParticipantNotFound):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="Could not find the participant with the specified id")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the deletion of Participant")

        return ParticipantDeletedResponse(participant=result.ok_value)

    async def create_participant(
        self, response: Response, input_data: ParticipantRequestBody
    ) -> ParticipantRegisteredResponse | ErrResponse:
        if input_data.is_admin and input_data.team_name:
            result = await self._service.register_admin_participant(input_data)

        # TODO: Implement this when the invite participant case is done
        # elif input_data.is_admin is False and input_data.team_name:
        #     result = await self._service.register_invite_participant(input_data)

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

        return ParticipantRegisteredResponse(participant=result.ok_value[0], team=result.ok_value[1])
