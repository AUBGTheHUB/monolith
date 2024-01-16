import json
from typing import Any, Dict, Tuple

from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon.teams_controller import TeamsController
from py_api.database.initialize import participants_col, t_col
from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.functionality.hackathon.participants_base import ParticipantsFunctionality
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models import NewParticipant, UpdateParticipant
from py_api.utilities.parsers import filter_none_values
from starlette.responses import JSONResponse


class ParticipantsController:
    @classmethod
    def get_all_participants(cls) -> JSONResponse:
        participants = list(participants_col.find())

        if not participants:
            return JSONResponse(
                content={"message": "No participants were found!"},
                status_code=404,
            )

        # the dumps funtion from bson.json_util returns a string
        return JSONResponse(
            content={"participants": json.loads(dumps(participants))},
            status_code=200,
        )

    @classmethod
    def get_specified_participant(cls, object_id: str) -> JSONResponse:
        try:
            specified_participant = participants_col.find_one(
                filter={"_id": ObjectId(object_id)},
            )

        except (InvalidId, TypeError) as e:
            return JSONResponse(
                content={"message": "Invalid object_id format!"},
                status_code=400,
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

        # ! You're not checking success state here!!!
        TeamFunctionality.update_team_query_using_dump(team.model_dump())

        return {"message": "The participant was deleted successfully from team!"}, 200

    @classmethod
    def update_participant(
        cls,
        object_id: str,
        participant_form: UpdateParticipant,
    ) -> JSONResponse:

        # filters the values set to None in the model
        fields_to_be_updated = filter_none_values(participant_form)

        # Queries the given participant and updates it
        try:
            to_be_updated_participant = participants_col.find_one_and_update(
                {"_id": ObjectId(object_id)}, {
                    "$set": fields_to_be_updated,
                },
                return_document=True,
            )

        except (InvalidId, TypeError) as e:
            return JSONResponse(
                content={"message": "Invalid object_id format!"},
                status_code=400,
            )

        if not to_be_updated_participant:
            return JSONResponse(
                content={"message": "The targeted participant was not found!"},
                status_code=404,
            )

        return JSONResponse(
            content={
                "participant": json.loads(dumps(to_be_updated_participant)),
            },
            status_code=200,
        )

    @classmethod
    def add_participant(cls, participant: NewParticipant, jwt_token: str | None = None) -> JSONResponse:
        if ParticipantsFunctionality.check_if_email_exists(participant.email):
            return JSONResponse(status_code=400, content={"message": "User with such email already exists"})

        if jwt_token:
            try:
                decoded_token = JWTFunctionality.decode_token(jwt_token)

            except Exception as e:
                return JSONResponse(status_code=401, content={"message": "JWT was provided, but is invalid", "reason": str(e)})

            team_name = decoded_token.get("team_name")

            team = TeamFunctionality.fetch_team(team_name=team_name)

            if not team:
                return JSONResponse(status_code=404, content={"message": "Can't find participant's team"})

            if len(team.team_members) >= 6:
                return JSONResponse(status_code=409, content={"message": "Can't register new team member. Team is at max capacity"})

            participant.is_verified = True
            participant.is_admin = False

            inserted_participant = ParticipantsFunctionality.create_participant(
                participant,
            )

            if not inserted_participant:
                return JSONResponse(status_code=500, content={"message": "Failed inserting new participant"})

            team.team_members.append(str(inserted_participant.inserted_id))
            updatedTeam = TeamFunctionality.update_team_query_using_dump(
                team.model_dump(),
            )

            if not updatedTeam:
                return JSONResponse(status_code=500, content={"message": "Failed updating updated team in database"})

            participant.team_name = updatedTeam.team_name

            updated_participant = ParticipantsFunctionality.update_participant(
                id=str(inserted_participant.inserted_id), participant=participant,
            )

            if not updated_participant:
                return JSONResponse(status_code=500, content={"message": "Something went wrong updating the participant with new team"})

            return {"message": "Participant was successfully verified and appended to corresponding team"}

        if participant.team_name:
            participant.is_verified = False
            participant.is_admin = True

            inserted_participant = ParticipantsFunctionality.create_participant(
                participant,
            )

            if not inserted_participant:
                return JSONResponse(status_code=500, content={"message": "Failed inserting new participant"})

            if TeamFunctionality.get_count_of_teams() > 15:
                return JSONResponse(content={"message": "Hackathon is at max capacity"}, status_code=409)

            team_object = TeamFunctionality.create_team_object_with_admin(
                user_id=str(inserted_participant.inserted_id), team_name=participant.team_name,
            )

            if not team_object:
                # or might be a bad transaction
                return JSONResponse(content={"message": "Name is already taken"}, status_code=400)

            new_team = TeamFunctionality.insert_team(team_object)

            if not new_team:
                # delete redundant participant document if team creation request has failed
                ParticipantsFunctionality.delete_participant(
                    str(inserted_participant.inserted_id),
                )

                return JSONResponse(status_code=500, content={"message": "Failed inserting new team. Participant entry was discarded."})

            """
                jwt_token = JWTFunctionality.create_jwt_token(
                    participant.team_name,
                )

                * generate token and send verification link via email to the participant
                # TODO: send_verification_email(to=participant.email, is_admin=True, verification_link=verification_link)

            """

            return {"message": "New admin participant was registered"}

        else:
            # Fetch the teams of type random
            random_teams = TeamFunctionality.fetch_teams_by_condition(
                {"team_type": "random"},
            )

            # Find the teams which can accept a new participant
            for team in random_teams:

                if (len(team.team_members) < 6):
                    avaliable_team = team
                    try:
                        # Creates new participant
                        new_participant = ParticipantsFunctionality.create_participant(
                            participant,
                        )
                        new_participant_object_id = str(
                            new_participant.inserted_id,
                        )
                        # Adds the participant to the team
                        avaliable_team = TeamFunctionality.add_participant_to_team_object(
                            avaliable_team.team_name, new_participant_object_id,
                        )
                        cls.update_participant(
                            new_participant_object_id, UpdateParticipant(
                                **{"team_name": avaliable_team.team_name}
                            ),
                        )
                        TeamFunctionality.update_team_query_using_dump(
                            avaliable_team.model_dump(),
                        )
                        return JSONResponse(content=avaliable_team.model_dump(), status_code=200)

                    except (Exception) as e:
                        return JSONResponse(content={"message": e.args}, status_code=422)

            if (TeamFunctionality.get_count_of_teams() < 15):
                # Creates new participant
                new_participant = ParticipantsFunctionality.create_participant(
                    participant,
                )
                new_participant_object_id = str(new_participant.inserted_id)
                # Create New Team and assign the new participant to it
                newTeam = TeamFunctionality.create_team_object_with_admin(
                    user_id=new_participant_object_id, team_name=TeamFunctionality.generate_random_team_name(), generate_random_team=True,
                )

                if newTeam:
                    cls.update_participant(
                        new_participant_object_id, UpdateParticipant(
                            **{"team_name": newTeam.team_name}
                        ),
                    )
                    TeamFunctionality.insert_team(newTeam)
                    return JSONResponse(content=newTeam.model_dump(), status_code=200)
                else:
                    return JSONResponse(content={"message": "Couldn't create team, because a team of the same name already exists!"}, status_code=422)

            else:
                return JSONResponse(content={"message": "The maximum number of teams is reached."}, status_code=409)
