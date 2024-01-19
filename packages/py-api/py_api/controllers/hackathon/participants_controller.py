import json
from typing import Any, Dict, Tuple

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models import NewParticipant, UpdateParticipant
from py_api.models.hackathon_teams_models import HackathonTeam
from py_api.services.mailer import send_mail


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
        specified_participant = participants_col.find_one(
            filter={"_id": ObjectId(object_id)},
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
        deleted_participant: Dict[str, Any] = participants_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not deleted_participant:
            return JSONResponse(
                content={"message": "The targeted participant was not found!"},
                status_code=404,
            )

        response, status_code = cls.delete_participant_from_team(
            deleted_participant,
        )
        if status_code != 200:
            return JSONResponse(response, status_code)

        return JSONResponse(
            content={"message": "The participant was deleted successfully!"},
            status_code=200,
        )

    @classmethod
    def delete_participant_from_team(cls, deleted_participant: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
        team = TeamFunctionality.fetch_team(
            deleted_participant.get("team_name"),
        )
        if not team:
            return {"message": "The participant is not in a team"}, 404

        deleted_participant_id = str(deleted_participant["_id"])

        if deleted_participant_id in team.team_members:
            team.team_members.remove(deleted_participant_id)
        else:
            return {"message": "The participant is not in the specified team"}, 404

        updated_team = TeamFunctionality.update_team_query_using_dump(
            team.model_dump(),
        )
        if not updated_team:
            return {"message": "Something went wrong updating team document"}, 500

        return {"message": "The participant was deleted successfully from team!"}, 200

    @classmethod
    def update_participant(
            cls,
            object_id: str,
            info_to_be_updated: UpdateParticipant,
    ) -> JSONResponse:

        # Queries the given participant and updates it
        updated_participant = ParticipantsFunctionality.update_participant(
            object_id, info_to_be_updated,
        )

        if not updated_participant:
            return JSONResponse(
                content={"message": "The targeted participant was not found!"},
                status_code=404,
            )

        return JSONResponse(
            content={
                "participant": json.loads(dumps(updated_participant)),
            },
            status_code=200,
        )

    @classmethod
    async def add_participant(cls, participant: NewParticipant, jwt_token: str | None = None) -> JSONResponse | Dict[
        str, str,
    ]:

        if TeamFunctionality.get_count_of_teams() > 15:
            return JSONResponse(content={"message": "Hackathon is at max capacity"}, status_code=409)

        if ParticipantsFunctionality.check_if_email_exists(participant.email):
            return JSONResponse(status_code=400, content={"message": "User with such email already exists"})

        if jwt_token:
            # The jwt token is provided as a query_param when a participant is registering via the custom form in
            # the frontend
            return await cls.handle_registration_via_invite_link(jwt_token, participant)

        # The participant has provided a team name upon registration, so we assign them as admin to the newly
        # created team
        if participant.team_name:
            participant.is_admin = True
            return await cls.add_participant_to_new_team(participant)

        # The participant hasn't provided a team name upon registration, so we follow the workflow for creating
        # and adding random patricians to teams
        else:
            # Fetch the teams of type random
            random_teams = TeamFunctionality.fetch_teams_by_condition(
                {"team_type": "random"},
            )

            # Find the teams which can accept a new participant
            for team in random_teams:
                if len(team.team_members) < 6:
                    return await cls.add_participant_to_existing_team(team, participant)

            # If all the random teams are full, check if there is space for creating a new one
            if TeamFunctionality.get_count_of_teams() < 15:
                return await cls.add_participant_to_new_team(participant, generate_random_team=True)

            return JSONResponse(content={"message": "The maximum number of teams is reached."}, status_code=409)

    @classmethod
    async def handle_registration_via_invite_link(cls, jwt_token: str, participant: NewParticipant) -> JSONResponse:
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
            return await cls.add_participant_to_existing_team(team, participant, is_invite=True)

        return JSONResponse(content={"message": "The maximum number of teams is reached."}, status_code=409)

    @classmethod
    async def add_participant_to_existing_team(
            cls, existing_team: HackathonTeam,
            participant: NewParticipant, is_invite: bool = False,
    ) -> JSONResponse:
        try:
            # Creates new participant
            new_participant = ParticipantsFunctionality.insert_participant(
                participant,
            )
            new_participant_object_id = str(new_participant.inserted_id)

            # Adds the participant to the team object
            existing_team = TeamFunctionality.add_participant_to_team_object(
                existing_team.team_name, new_participant_object_id,
            )

            # We assume that when the participant is registering via a link in the body of the request we
            # will have the team_name passed
            if not is_invite:
                updated_participant = ParticipantsFunctionality.update_participant(
                    new_participant_object_id, UpdateParticipant(
                        team_name=existing_team.team_name,
                    ),
                )
                if not updated_participant:
                    return JSONResponse(
                        content={
                            "message": "Something went wrong updating participant document",
                        },
                        status_code=500,
                    )

            existing_team = TeamFunctionality.update_team_query_using_dump(
                existing_team.model_dump(),
            )
            if not existing_team:
                return JSONResponse(content={"message": "Something went wrong updating team document"}, status_code=500)

            if not is_invite:
                jwt_token = JWTFunctionality.create_jwt_token(
                    new_participant_object_id, existing_team.team_name,
                )
                await send_mail(
                    participant.email, "Test",
                    f"Token: {JWTFunctionality.get_verification_link(jwt_token)}",
                )
                # background_tasks = BackgroundTasks()
                # background_tasks.add_task(background_send_mail, participant.email, "Test",
                #                           f"Url: {JWTFunctionality.get_verification_link(jwt_token)}")

            return JSONResponse(content=existing_team.model_dump(), status_code=200)

        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    @classmethod
    async def add_participant_to_new_team(
            cls, participant: NewParticipant,
            generate_random_team: bool = False,
    ) -> JSONResponse:
        try:
            # Creates new participant
            new_participant = ParticipantsFunctionality.insert_participant(
                participant,
            )
            new_participant_object_id = str(new_participant.inserted_id)

            # Create New Random Team and assigns the new participant to it
            new_team = TeamFunctionality.create_team_object_with_admin(
                user_id=new_participant_object_id,
                team_name=TeamFunctionality.generate_random_team_name(
                ) if generate_random_team else participant.team_name,
                generate_random_team=generate_random_team,
            )
            if not new_team:
                return JSONResponse(
                    content={
                        "message": "Couldn't create team, because a team of the same name already exists!",
                    },
                    status_code=422,
                )

            updated_participant = ParticipantsFunctionality.update_participant(
                new_participant_object_id, UpdateParticipant(
                    team_name=new_team.team_name,
                ),
            )
            if not updated_participant:
                return JSONResponse(
                    content={
                        "message": "Something went wrong updating participant document",
                    },
                    status_code=500,
                )

            team_insert_result = TeamFunctionality.insert_team(new_team)
            if not team_insert_result:
                # delete redundant participant document if team creation request has failed
                ParticipantsFunctionality.delete_participant(
                    str(new_participant_object_id),
                )
                return JSONResponse(
                    status_code=500, content={
                        "message": "Failed inserting new team. Participant entry was discarded.",
                    },
                )

            jwt_token = JWTFunctionality.create_jwt_token(
                new_participant_object_id, new_team.team_name,
            )
            await send_mail(participant.email, "Test", f"Token: {JWTFunctionality.get_verification_link(jwt_token)}")
            # background_tasks = BackgroundTasks()
            # background_tasks.add_task(background_send_mail, participant.email, "Test",
            #                           f"Url: {JWTFunctionality.get_verification_link(jwt_token)}")

            return JSONResponse(content=new_team.model_dump(), status_code=200)

        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)