from result import is_err
from src.server.handlers.base_handler import BaseHandler
from src.service.participants_verification_service import ParticipantVerificationService
from starlette import status
from src.utils import JwtUtility
from src.server.schemas.response_schemas.schemas import ErrResponse, ParticipantVerifiedResponse, Response
from src.server.schemas.jwt_schemas.schemas import JwtParticipantVerification


class VerificationHandlers(BaseHandler):

    def __init__(self, service: ParticipantVerificationService) -> None:
        self._service = service

    async def verify_participant(self, jwt_token: str) -> Response:
        # We decode the token here so that we can determine the case of verfication that we
        # are dealing with: `admin verification` or `random participant verification`.
        result = JwtUtility.decode_data(token=jwt_token, schema=JwtParticipantVerification)

        if is_err(result):
            return self.handle_error(result.err_value)

        jwt_payload = result.ok_value

        if jwt_payload["is_admin"]:
            return Response(response_model=ErrResponse("This feature is not yet implemented!"), status_code=501)

        else:
            result = await self._service.verify_random_participant(jwt_data=jwt_payload)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=ParticipantVerifiedResponse(participant=result.ok_value[0], team=result.ok_value[1]),
            status_code=status.HTTP_200_OK,
        )
