import json
from typing import Any, Dict, Tuple

from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon_teams_controller import TeamsController
from py_api.database.initialize import participants_col, t_col
from py_api.functionality.hackathon.teams.teams_utility_functions import TeamsUtilities
from py_api.functionality.hackathon.verification.jwt_verification import JWTVerification
from py_api.models import NewParticipant, UpdateParticipant
from py_api.utilities.parsers import filter_none_values
from pymongo.results import InsertOneResult
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
        team = TeamsUtilities.fetch_team(deleted_participant.get("team_name"))
        if not team:
            return {"message": "The participant is not in a team"}, 404

        deleted_participant_id = str(deleted_participant["_id"])

        if deleted_participant_id in team.team_members:
            team.team_members.remove(deleted_participant_id)
        else:
            return {"message": "The participant is not in the specified team"}, 404

        TeamsUtilities.update_team_query(team.model_dump())

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
    def add_participant(cls, participant: NewParticipant, jwt_token: str) -> JSONResponse:

        if jwt_token:
            # TODO: implement logic for adding participant to team
            # * verify team capacity
            # * verify jwt
            return

        if participant.team_name:
            if participants_col.find_one(filter={"email": participant.email}):
                return JSONResponse(
                    content={
                        "message": "The email of the participant already exists!",
                    },
                    status_code=409,
                )

            # TODO: create unverified participant
            # TODO: create unverified team and append participant

            jwt_token = JWTVerification.create_jwt_token(participant.team_name)
            # TODO: verification_link = JWTVerification.create_admin_verification_link(jwt_token)

            # TODO: send_verification_email(to=participant.email, is_admin=True, verification_link=verification_link)
            # * is_admin will identify whether the used template should be for admins who have to verify their teams
            # * or the one storing the link for inviting participants to the team

        else:
            # TODO: create participant
            # TODO: assign to RANDOM team if there's one with free space or create new one
            return

        return JSONResponse(
            content={"message": "The participant was successfully added!"},
            status_code=200,
        )
