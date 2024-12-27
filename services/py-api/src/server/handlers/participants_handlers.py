from typing import Optional
from result import is_err
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData
from src.utils import JwtUtility
from starlette import status
from starlette.responses import Response

from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
)
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
)
from src.service.participants_registration_service import ParticipantRegistrationService


class ParticipantHandlers:

    def __init__(self, service: ParticipantRegistrationService) -> None:
        self._service = service

    async def create_participant(
        self, response: Response, input_data: ParticipantRequestBody, jwt_token: Optional[str] = None,
    ) -> ParticipantRegisteredResponse | ErrResponse:
        
        if input_data.is_admin and input_data.team_name:
            result = await self._service.register_admin_participant(input_data)

        elif input_data.is_admin is False and input_data.team_name:
            # Decode the token
            decoded_result = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)
            if is_err(decoded_result):
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return ErrResponse(error=f"JWT decoding failed: {decoded_result.err_value}")
            
            decoded_data = decoded_result.ok_value
            team_name_from_token = decoded_data["team_id"]

            if input_data.team_name != team_name_from_token:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return ErrResponse(error="Team name in request does not match the invite link.")
            
            result = await self._service.register_invite_link_participant(input_data)

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
            
            if isinstance(result.err_value, TeamCapacityExceededError):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Your team's capacity has been reached")

            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrResponse(error="An unexpected error occurred during the creation of Participant")

        return ParticipantRegisteredResponse(participant=result.ok_value[0], team=result.ok_value[1])
