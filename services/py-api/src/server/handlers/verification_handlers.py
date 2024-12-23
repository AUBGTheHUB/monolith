from result import is_err
from fastapi import Response
from starlette import status

from src.utils import JwtUtility
from src.server.exception import HackathonCapacityExceededError
from src.service.verification_service import VerificationService
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData


class VerificationHandlers:
    def __init__(self, verification_service: VerificationService) -> None:
        self._verification_service = verification_service

    async def verifyParticipant(self, response: Response, jwt_token: str) -> Response | ErrResponse:
        jwt_payload = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)

        if is_err(jwt_payload):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrResponse(error=jwt_payload.err_value)

        participant_id = jwt_payload.ok_value.get("sub")

        participant_exists = await self._verification_service.verify_participant_exists(id=participant_id)
        if not participant_exists:
            response.status_code = status.HTTP_409_CONFLICT
            return ErrResponse(error="Participant does not exist in database")

        if jwt_payload.ok_value.get("is_admin"):
            result = await self._verification_service.verify_admin_participant(participant_id)

            if is_err(result):
                if isinstance(result.err_value, HackathonCapacityExceededError):
                    response.status_code = status.HTTP_409_CONFLICT
                    return ErrResponse(error="Max hackathon capacity has been reached")
                response.status_code = 500
                return ErrResponse(
                    error="An unexpected error occurred during the verification of the admin participant"
                )

            return Response(content="Successfully verifyed admin participant")
        #  Validation check for random participants
        return ErrResponse(error="Not implemented yet")
