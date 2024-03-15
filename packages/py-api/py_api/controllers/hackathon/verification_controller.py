from typing import Any, Dict

from fastapi.responses import JSONResponse
from py_api.database.database_transaction_handlers import (
    handle_database_session_transaction,
)
from py_api.functionality.hackathon.jwt_base import JWTFunctionality, JWTType
from py_api.functionality.hackathon.mailing_functionality import MailingFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models import HackathonTeam
from py_api.models.hackathon_participants_models import (
    NewParticipant,
    UpdateParticipant,
)
from pymongo.client_session import ClientSession
from starlette.background import BackgroundTasks


class VerificationController:
    @classmethod
    @handle_database_session_transaction
    def verify_participants(cls, jwt_token: str, session: ClientSession) -> JSONResponse:
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
            # Fetch the teams of type random
            random_teams = TeamFunctionality.fetch_teams_by_condition(
                {"team_type": "random"},
            )

            # Find the teams which can accept a new participant and add it if there is space
            for team in random_teams:
                if len(team.team_members) < 6:
                    return cls.add_participant_to_existing_team(
                        verified_participant, team, session,
                        decoded_token, background_tasks, jwt_token,
                    )

            # Create a new random team if needed
            return cls.create_team_and_send_email(
                decoded_token, session, background_tasks, verified_participant, True, jwt_token,
            )

        if decoded_token.get("team_name") and decoded_token.get("random_participant") is False and decoded_token.get(
                "invite",
        ) is False:
            # A confirmation email is send to the admin along with the invite link
            jwt_token = JWTFunctionality.create_jwt_token(
                team_name=decoded_token.get("team_name"), is_invite=True,
            )
            return cls.create_team_and_send_email(
                decoded_token, session, background_tasks, verified_participant, False, jwt_token,
            )

    @classmethod
    def create_team_and_send_email(
        cls, decoded_token: JWTType, session: ClientSession,
        background_tasks: BackgroundTasks,
        verified_participant: Dict[str, Any], generate_random_team: bool,
        jwt_token: str,
    ) -> JSONResponse:
        new_team = cls.create_new_team(
            new_participant_object_id=str(decoded_token.get("sub")), session=session,
            generate_random_team=generate_random_team,
            team_name=decoded_token.get("team_name"),
        )

        if generate_random_team:
            cls.send_confirmation_email(
                background_tasks, verified_participant, jwt_token, None,
            )
        else:
            cls.send_confirmation_email(
                background_tasks, verified_participant, jwt_token, new_team.team_name,
            )

        return JSONResponse(
            content={
                "message": f"Participant was successfully verified and has been added to team "
                           f"{new_team.team_name}",
            },
            status_code=200,
            background=background_tasks,
        )

    @classmethod
    def send_confirmation_email(
        cls, background_tasks: BackgroundTasks, verified_participant: Dict[str, Any],
        jwt_token: str,
        team_name: str | None,
    ) -> None:
        background_tasks.add_task(
            MailingFunctionality.send_confirmation_email, email=verified_participant.get(
                "email",
            ),
            jwt_token=jwt_token,
            team_name=team_name,
            participant_name=verified_participant.get("first_name"), is_admin=verified_participant.get("is_admin"),
        )

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

    @classmethod
    def add_participant_to_existing_team(
        cls, participant: Dict[str, Any], existing_team: HackathonTeam,
        session: ClientSession, decoded_token: JWTType,
        background_tasks: BackgroundTasks, jwt_token: str,
        is_invite: bool = False,
    ) -> JSONResponse:

        result = TeamFunctionality.add_participant_to_team_object(
            existing_team.team_name, decoded_token["sub"],
        )

        if not isinstance(result, HackathonTeam):
            return JSONResponse(content=result[0], status_code=result[1])

        existing_team = TeamFunctionality.update_team_query_using_dump(
            result.model_dump(), session=session,
        )
        cls.send_confirmation_email(
            background_tasks, participant, jwt_token, None,
        )

        return JSONResponse(content=existing_team.model_dump(), status_code=200, background=background_tasks)
