from typing import Any, Dict

from fastapi.responses import JSONResponse
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_participants_models import UpdateParticipant
from py_api.services.mailer import send_email_background_task
from starlette.background import BackgroundTasks


class VerificationController:
    @classmethod
    def verify_participants(cls, jwt_token: str) -> JSONResponse | Dict[str, str]:
        background_tasks = BackgroundTasks()

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

        if team.is_verified is not True:
            team.is_verified = True
            TeamFunctionality.update_team_query_using_dump(
                team_payload=team.model_dump(),
            )

        try:
            if team.team_type == team.team_type.NORMAL:
                # Invite link is sent to the admin along with verification message
                jwt_token = JWTFunctionality.create_jwt_token(
                    team_name=team.team_name, is_invite=True,
                )

                background_tasks.add_task(
                    send_email_background_task, verified_participant.get(
                        "email",
                    ), "Test",
                    f"You have successfully registred from HACKAUBG 6.0. To invite your teamates to join your team use the following link. \n Url: {JWTFunctionality.get_email_link(jwt_token, for_frontend=True, is_invite=True)}",
                )

            else:
                # Verification email is sent to the random team participant
                background_tasks.add_task(
                    send_email_background_task, verified_participant.get(
                        "email",
                    ), "HackAUBG registration confirmation",
                    f"You have successfully been registred to HACKAUBG 6.0! Happy Coding!",
                )

        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=500,
            )

        return JSONResponse(
            content={"message": "Participant was successfully verified"}, status_code=200,
            background=background_tasks,
        )

    @classmethod
    def test_controller(cls, team_name: str) -> Any:
        return {"token": JWTFunctionality.create_jwt_token(team_name)}
