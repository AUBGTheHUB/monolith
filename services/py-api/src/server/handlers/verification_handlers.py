from result import is_err
from fastapi import Response
from src.service.hackathon_service import HackathonService
from starlette import status

from src.utils import JwtUtility
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData


class VerificationHandlers:
    def __init__(self, hackaton_service: HackathonService) -> None:
        self._hackaton_service = hackaton_service

    async def verify_participant(self, response: Response, jwt_token: str) -> Response | ErrResponse:
        jwt_payload = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)

        if is_err(jwt_payload):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrResponse(error=jwt_payload.err_value)

        participant_id = jwt_payload.ok_value.get("sub")

        participant_exists = await self._hackaton_service.check_if_participant_exists_in_by_id(object_id=participant_id)

        if not participant_exists:
            response.status_code = status.HTTP_404_NOT_FOUND
            return ErrResponse(error="Participant does not exist in database")

        if jwt_payload.ok_value.get("is_admin"):

            has_capacity = await self._hackaton_service.check_capacity_register_admin_participant_case()
            if not has_capacity:
                response.status_code = status.HTTP_409_CONFLICT
                return ErrResponse(error="Max hackathon capacity has been reached")

            team_id = jwt_payload.ok_value.get("team_id")
            result = await self._hackaton_service.verify_admin_participant_and_team_in_transaction(
                admin_id=participant_id, team_id=team_id
            )

            if is_err(result):
                return ErrResponse(
                    error="An unexpected error occurred during the verification of the admin participant"
                )

            return Response(content="Successfully verified admin participant")
        #  Validation check for random participants
        return ErrResponse(error="Not implemented yet")
