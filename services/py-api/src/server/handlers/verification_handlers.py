from result import is_err
from fastapi import Response
from src.server.exception import HackathonCapacityExceededError, ParticipantNotFoundError, TeamNotFoundError
from src.service.hackathon_service import HackathonService
from starlette import status

from src.utils import JwtUtility
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData


class VerificationHandlers:
    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def verify_participant(self, response: Response, jwt_token: str) -> Response | ErrResponse:
        jwt_payload = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)

        if is_err(jwt_payload):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrResponse(error=jwt_payload.err_value)

        participant_id = jwt_payload.ok_value.get("sub")
        is_admin = jwt_payload.ok_value.get("is_admin")
        team_id = jwt_payload.ok_value.get("team_id")

        result = await self._hackathon_service.verify_participant_and_team_in_transaction(
            is_admin=is_admin, participant_id=participant_id, team_id=team_id
        )

        if is_err(result):
            if isinstance(result.err_value, HackathonCapacityExceededError):
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Max hackathon capacity has been reached")
            if isinstance(result.err_value, ParticipantNotFoundError):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="The participant was not found")
            if isinstance(result.err_value, TeamNotFoundError):
                response.status_code = status.HTTP_404_NOT_FOUND
                return ErrResponse(error="The team was not found")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrResponse(error="An unexpected error occurred during the verification of the participant")

        return Response(content="Successfully verified participant")
