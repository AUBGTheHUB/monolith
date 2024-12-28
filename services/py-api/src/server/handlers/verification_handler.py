from result import is_err
from fastapi import Response
from starlette import status
from src.utils import JwtUtility
from src.service.hackathon_service import HackathonService
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData


class VerificationHandlers:
    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def verify_participant(self, response: Response, jwt_token: str) -> Response | ErrResponse:
        # Decode the JWT token using JwtUtility
        jwt_payload = JwtUtility.decode_data(token=jwt_token, schema=JwtUserData)

        if is_err(jwt_payload):
            # Invalid or expired JWT token
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrResponse(error=jwt_payload.err_value)

        # Extract necessary fields from the decoded payload
        participant_id = jwt_payload.ok_value.get("sub")
        is_admin = jwt_payload.ok_value.get("is_admin")
        team_id = jwt_payload.ok_value.get("team_id")

        # Validate participant existence
        participant_exists = await self._hackathon_service.check_if_participant_exists_in_by_id(participant_id)
        if not participant_exists:
            response.status_code = status.HTTP_404_NOT_FOUND
            return ErrResponse(error="Participant does not exist in the database.")

        # Random participant verification
        if not is_admin:
            if not team_id:
                # Perform Capacity Check 1 for random participants
                has_capacity = await self._hackathon_service.check_capacity_register_random_participant_case()
                if not has_capacity:
                    response.status_code = status.HTTP_409_CONFLICT
                    return ErrResponse(error="Hackathon capacity is full.")

            # Verify random participant
            result = await self._hackathon_service.verify_random_participant_and_update(participant_id)
            if is_err(result):
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return ErrResponse(error="Failed to verify the random participant.")

            return Response(content="Successfully verified random participant", status_code=status.HTTP_200_OK)

        # Admin participant verification logic can be implemented if required
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrResponse(error="Invalid token for admin participant verification.")
