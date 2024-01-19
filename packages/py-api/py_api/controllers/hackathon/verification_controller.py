from typing import Any, Dict

from fastapi.responses import JSONResponse
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_participants_models import UpdateParticipant
from py_api.services.mailer import send_mail
from starlette.background import BackgroundTasks


class VerificationController:
    @classmethod
    async def verify_participants(cls, jwt_token: str) -> JSONResponse | Dict[str, str]:
        result = JWTFunctionality.decode_token(jwt_token)

        if isinstance(result, dict):
            decoded_token = result
        else:
            return JSONResponse(content=result[0], status_code=result[1])

        team = TeamFunctionality.fetch_team(
            team_name=decoded_token.get("team_name"),
        )
        if not team:
            return JSONResponse(
                content={
                    "message": "Cannot verify participant as such team doesn't exist",
                },
                status_code=404,
            )

        verified_participant = ParticipantsFunctionality.update_participant(
            object_id=str(decoded_token.get("sub")), participant=UpdateParticipant(
                is_verified=True,
            ),
        )
        if not verified_participant:
            return JSONResponse(
                content={
                    "message": "Something went wrong updating participant document",
                },
                status_code=500,
            )

        if team.is_verified is not True:
            team.is_verified = True
            verified_team = TeamFunctionality.update_team_query_using_dump(
                team_payload=team.model_dump(),
            )

            if not verified_team:
                return JSONResponse(
                    content={
                        "message": "Something went wrong updating team document",
                    },
                    status_code=500,
                )

        if team.team_type == team.team_type.NORMAL:
            try:
                jwt_token = JWTFunctionality.create_jwt_token(
                    team_name=team.team_name, is_invite=True,
                )
                await send_mail(
                    verified_participant.get("email"), "Test",
                    f"Token: {JWTFunctionality.get_verification_link(jwt_token)}",
                )
                # background_tasks = BackgroundTasks()
                # background_tasks.add_task(background_send_mail, verified_participant.get("email"), "Test",
                #                           f"Url: {JWTFunctionality.get_verification_link(jwt_token)}")
            except Exception as e:
                return JSONResponse(
                    content={"error": str(e)},
                    status_code=500,
                )
        return {"message": "Participant was successfully verified"}

    @classmethod
    def test_controller(cls, team_name: str) -> Any:
        return {"token": JWTFunctionality.create_jwt_token(team_name)}
