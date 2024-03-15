from typing import Any, Dict

from fastapi.responses import JSONResponse
from py_api.database.database_transaction_handlers import (
    handle_database_session_transaction,
)
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.mailing_functionality import MailingFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models import HackathonTeam
from py_api.models.hackathon_participants_models import UpdateParticipant
from pymongo.client_session import ClientSession
from starlette.background import BackgroundTasks


class VerificationController:
    @classmethod
    @handle_database_session_transaction
    def verify_participants(cls, jwt_token: str, session: ClientSession) -> JSONResponse | Dict[str, str]:
        background_tasks = BackgroundTasks()

        result = JWTFunctionality.decode_token(jwt_token)

        if isinstance(result, dict):
            decoded_token = result
        else:
            return JSONResponse(content=result[0], status_code=result[1])

        participant = ParticipantsFunctionality.get_participant_by_id(
            str(decoded_token.get("sub")),
        )
        if not participant:
            return JSONResponse(
                content={"message": "Participant with such id does not exist"},
                status_code=208,
            )

        if participant.get("is_verified") is True:
            return JSONResponse(
                content={"message": "Participant is already verified"},
                status_code=208,
            )

        verified_participant: Dict[str, Any] = ParticipantsFunctionality.update_participant(
            object_id=str(decoded_token.get("sub")), participant=UpdateParticipant(
                is_verified=True,
            ), session=session,
        )

        if decoded_token.get("team_name") is None and decoded_token.get("random_participant") is True:
            new_random_team = cls.create_new_team(
                new_participant_object_id=str(decoded_token.get("sub")), session=session, generate_random_team=True,
                team_name=None,
            )

            # A confirmation email is send to the random participant
            background_tasks.add_task(
                MailingFunctionality.send_confirmation_email, email=verified_participant.get(
                    "email",
                ),
                jwt_token=jwt_token,
                team_name=None,
                is_admin=False,
                participant_name=verified_participant.get("first_name"),
            )

            return JSONResponse(
                content={
                    "message": f"Random participant was successfully verified and has been added to team "
                               f"{new_random_team.team_name}",
                },
                status_code=200,
                background=background_tasks,
            )

        if decoded_token.get("team_name") and decoded_token.get("random_participant") is False and decoded_token.get(
                "invite",
        ) is False:
            new_team = cls.create_new_team(
                new_participant_object_id=str(decoded_token.get("sub")), session=session, generate_random_team=False,
                team_name=decoded_token.get("team_name"),
            )

            # A confirmation email is send to the admin along with the invite link
            jwt_token = JWTFunctionality.create_jwt_token(
                team_name=new_team.team_name, is_invite=True,
            )

            background_tasks.add_task(
                MailingFunctionality.send_confirmation_email, email=verified_participant.get(
                    "email",
                ),
                jwt_token=jwt_token,
                team_name=verified_participant.get("team_name"),
                participant_name=verified_participant.get("first_name"), is_admin=True,
            )

            return JSONResponse(
                content={
                    "message": f"Admin participant was successfully verified and has been added to team "
                               f"{new_team.team_name}",
                },
                status_code=200,
                background=background_tasks,
            )

        # team = TeamFunctionality.fetch_team(
        #     team_name=decoded_token.get("team_name"),
        # )
        # if not team:
        #     return JSONResponse(
        #         content={
        #             "message": "Cannot verify participant as such team doesn't exist",
        #         },
        #         status_code=404,
        #     )
        #
        # if team.is_verified is not True:
        #     team.is_verified = True
        #     TeamFunctionality.update_team_query_using_dump(
        #         team_payload=team.model_dump(),
        #     )
        #
        # try:
        #     if team.team_type == team.team_type.NORMAL:
        #         # A confirmation email is send to the admin along with the invite link
        #         jwt_token = JWTFunctionality.create_jwt_token(
        #             team_name=team.team_name, is_invite=True,
        #         )
        #
        #         background_tasks.add_task(
        #             MailingFunctionality.send_confirmation_email, email=verified_participant.get(
        #                 "email",
        #             ),
        #             jwt_token=jwt_token,
        #             team_name=verified_participant.get("team_name"),
        #             participant_name=verified_participant.get("first_name"), is_admin=True,
        #         )
        #
        #     else:
        # # A confirmation email is send to the random participant
        #
        # except Exception as e:
        #     return JSONResponse(
        #         content={"error": str(e)},
        #         status_code=500,
        #     )

        return JSONResponse(
            content={"message": "Participant was successfully verified"}, status_code=200,
            background=background_tasks,
        )

    @classmethod
    def test_controller(cls, team_name: str) -> Any:
        return {"token": JWTFunctionality.create_jwt_token(team_name)}

    @classmethod
    def create_new_team(
        cls, new_participant_object_id: str, session: ClientSession,
        generate_random_team: bool, team_name: str | None = None,
    ) -> HackathonTeam:
        """
        Creates a new random team with the participant and inserts it into the database

        Returns a new team object"""

        new_team_obj = TeamFunctionality.create_team_object_with_first_participant(
            user_id=new_participant_object_id,
            team_name=team_name,
            generate_random_team=generate_random_team,
        )

        TeamFunctionality.insert_team(new_team_obj, session)

        return new_team_obj
