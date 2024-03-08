import json
from typing import Any, Callable, Dict

from bson.json_util import dumps
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from py_api.database.database_transaction_handlers import (
    handle_database_session_transaction,
)
from py_api.database.initialize import client, participants_col
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models import NewParticipant, UpdateParticipant
from py_api.models.hackathon_teams_models import HackathonTeam
from py_api.services.mailer import send_email_background_task
from pymongo.client_session import ClientSession


class ParticipantsController:
    @classmethod
    def get_all_participants(cls) -> JSONResponse:
        participants = list(participants_col.find())

        if not participants:
            return JSONResponse(
                content={"message": "No participants were found!"},
                status_code=404,
            )

        # the dumps function from bson.json_util returns a string
        return JSONResponse(
            content={"participants": json.loads(dumps(participants))},
            status_code=200,
        )

    @classmethod
    def get_specified_participant(cls, object_id: str) -> JSONResponse:
        specified_participant = ParticipantsFunctionality.get_participant_by_id(
            object_id,
        )

        if not specified_participant:
            return JSONResponse(
                content={"message": "The targeted participant was not found!"},
                status_code=404,
            )

        return JSONResponse(
            content={"participant": json.loads(dumps(specified_participant))},
            status_code=200,
        )

    @classmethod
    def delete_participant(cls, object_id: str) -> JSONResponse:
        try:
            participant = ParticipantsFunctionality.get_participant_by_id(
                object_id,
            )
            if not participant:
                return JSONResponse(
                    content={
                        "message": "The targeted participant was not found!",
                    },
                    status_code=404,
                )

            response, status_code = ParticipantsFunctionality.remove_participant_from_team(
                object_id, str(NewParticipant(**participant).team_name),
            )

            ParticipantsFunctionality.delete_participant(object_id)

            if status_code != 200:
                return JSONResponse(response, status_code)

            return JSONResponse(
                content={"message": "The participant was deleted successfully!"},
                status_code=200,
            )

        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    @classmethod
    def update_participant(
            cls,
            object_id: str,
            info_to_be_updated: UpdateParticipant,
    ) -> JSONResponse:
        try:

            if not ParticipantsFunctionality.get_participant_by_id(object_id):
                return JSONResponse(
                    content={
                        "message": "The targeted participant was not found!",
                    },
                    status_code=404,
                )

            # Queries the given participant and updates it
            updated_participant = ParticipantsFunctionality.update_participant(
                object_id, info_to_be_updated,
            )

            return JSONResponse(
                content={
                    "participant": json.loads(dumps(updated_participant)),
                },
                status_code=200,
            )

        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    @classmethod
    def add_participant(cls, participant: NewParticipant, jwt_token: str | None = None) -> JSONResponse | Dict[
        str, str,
    ]:

        if ParticipantsFunctionality.check_if_email_exists(participant.email):
            return JSONResponse(status_code=400, content={"message": "User with such email already exists"})

        if jwt_token:
            # The jwt token is provided as a query_param when a participant is registering via the custom form in
            # the frontend
            return cls.handle_registration_via_invite_link(jwt_token, participant)

        # Logic for adding a random participant to an existing team
        if not participant.team_name:
            # Fetch the teams of type random
            random_teams = TeamFunctionality.fetch_teams_by_condition(
                {"team_type": "random"},
            )
            # Find the teams which can accept a new participant and add it if there is space
            for team in random_teams:
                if len(team.team_members) < 6:
                    return cls.add_participant_to_existing_team(participant, team)

        # Logic for creating a new team and adding the admin
        if TeamFunctionality.get_count_of_teams() < 16:
            if participant.team_name:
                # The participant has provided a team name upon registration, so we assign them as admin to the newly
                # created team
                return cls.add_participant_to_new_team(participant)
            else:
                # The participant hasn't provided a team name upon registration, so we assign the admin to the newly created random team
                return cls.add_participant_to_new_team(participant, generate_random_team=True)

        return JSONResponse(content={"message": "Hackathon is at maximum capacity"}, status_code=409)

    @classmethod
    def handle_registration_via_invite_link(cls, jwt_token: str, participant: NewParticipant) -> JSONResponse:
        result = JWTFunctionality.decode_token(jwt_token, is_invite=True)
        if isinstance(result, dict):
            decoded_token = result
        else:
            return JSONResponse(content=result[0], status_code=result[1])

        team = TeamFunctionality.fetch_team(
            team_name=decoded_token.get("team_name"),
        )

        if not team:
            return JSONResponse(content={"message": "Team with this name does not exist"}, status_code=404)

        if len(team.team_members) < 6:
            return cls.add_participant_to_existing_team(participant, team, is_invite=True)

        return JSONResponse(content={"message": "The maximum number of team members is reached."}, status_code=409)

    @classmethod
    @handle_database_session_transaction
    def add_participant_to_existing_team(
            cls, participant: NewParticipant, existing_team: HackathonTeam, session: ClientSession,
            is_invite: bool = False,
    ) -> JSONResponse:
        if is_invite:
            participant.is_verified = True

        participant.team_name = existing_team.team_name
        new_participant = ParticipantsFunctionality.insert_participant(
            participant, session,
        )

        new_participant_object_id = str(new_participant.inserted_id)

        result = TeamFunctionality.add_participant_to_team_object(
            existing_team.team_name, new_participant_object_id,
        )

        if not isinstance(result, HackathonTeam):
            return JSONResponse(content=result[0], status_code=result[1])

        existing_team = TeamFunctionality.update_team_query_using_dump(
            result.model_dump(), session=session,
        )

        background_tasks = BackgroundTasks()
        if not is_invite:
            jwt_token = JWTFunctionality.create_jwt_token(
                new_participant_object_id, existing_team.team_name,
            )
            background_tasks.add_task(
                send_email_background_task, participant.email, "Test",
                f"Url: {JWTFunctionality.get_email_link(jwt_token, for_frontend=True)}",
            )
        else:
            background_tasks.add_task(
                send_email_background_task, participant.email, "HackAUBG registration confirmation",
                f"You have successfully to {participant.team_name} on HACKAUBG 6.0! Happy Coding!",
            )

        return JSONResponse(content=existing_team.model_dump(), status_code=200, background=background_tasks)

    @classmethod
    @handle_database_session_transaction
    def add_participant_to_new_team(
            cls, participant: NewParticipant, session: ClientSession,
            generate_random_team: bool = False,
    ) -> JSONResponse:
        participant.is_admin = True
        new_participant = ParticipantsFunctionality.insert_participant(
            participant, session,
        )

        new_participant_object_id = str(new_participant.inserted_id)

        new_team = TeamFunctionality.create_team_object_with_admin(
            user_id=new_participant_object_id,
            team_name=TeamFunctionality.generate_random_team_name()
            if generate_random_team else participant.team_name,
            generate_random_team=generate_random_team,
        )
        if not new_team:
            session.abort_transaction()
            return JSONResponse(
                content={
                    "message": "Couldn't create team, because a team of the same name already exists!",
                },
                status_code=409,
            )

        TeamFunctionality.insert_team(new_team, session)

        jwt_token = JWTFunctionality.create_jwt_token(
            new_participant_object_id, new_team.team_name,
        )

        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            send_email_background_task, participant.email, "Test",
            f"Url: {JWTFunctionality.get_email_link(jwt_token)}",
        )

        return JSONResponse(content=new_team.model_dump(), status_code=200, background=background_tasks)
