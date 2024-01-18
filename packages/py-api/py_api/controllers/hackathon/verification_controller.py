from typing import Any, Dict

from fastapi.responses import JSONResponse
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_participants_models import UpdateParticipant


class VerificationController:
    @classmethod
    def verify_admin(cls, jwt_token: str) -> JSONResponse:
        try:
            decoded_token = JWTFunctionality.decode_token(jwt_token)
        except:
            return JSONResponse(status_code=401)

        team = TeamFunctionality.fetch_team(
            team_name=decoded_token.get("team_name"),
        )

        if not team:
            return JSONResponse(content={"message": "Cannot verify admin as such team doesn't exist"}, status_code=404)

        # TODO: verify expiration

        verified_admin = ParticipantsFunctionality.update_participant(
            id=team.team_members[0], participant=UpdateParticipant(
                is_verified=True,
            ),
        )

        if not verified_admin:
            return JSONResponse(content={"message": "Something went wrong updating admin document"}, status_code=500)

        # TODO: add is_verified property to teams so that you can later delete expired teams upon admin clean ups
        # TODO: send email with jwt link for appending participants to now verified team

        return {"message": "Admin was successfully verified"}

    @classmethod
    def test_controller(cls, team_name: str) -> Any:
        return {"token": JWTFunctionality.create_jwt_token(team_name)}
