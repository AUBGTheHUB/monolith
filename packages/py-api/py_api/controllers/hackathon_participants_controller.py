import json

from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon_teams_controller import TeamsController
from py_api.database.initialize import participants_col, t_col
from py_api.functionality.hackathon.teams.teams_utility_functions import TeamsUtilities
from py_api.models import NewParticipant, UpdateParticipant
from py_api.utilities.parsers import filter_none_values
from pymongo.results import InsertOneResult


class ParticipantsController:

    def get_all_participants() -> JSONResponse:
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

    def get_specified_participant(object_id: str) -> JSONResponse:
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

    def delete_participant(object_id: str) -> JSONResponse:
        deleted_participant = participants_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not deleted_participant:
            return JSONResponse(
                content={"message": "The targeted participant was not found!"},
                status_code=404,
            )

        return JSONResponse(
            content={"message": "The participant was deleted successfully!"},
            status_code=200,
        )

    def update_participant(
        object_id: str,
        participant_form: UpdateParticipant,
    ) -> JSONResponse:

        # filters the values set to None in the model
        fields_to_be_updated = filter_none_values(participant_form)

        # Queries the given participant and updates it
        to_be_updated_participant = participants_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": fields_to_be_updated,
            },
            return_document=True,
        )

        return JSONResponse(
            content={
                "participant": json.loads(dumps(to_be_updated_participant)),
            },
            status_code=200,
        )

    def add_participant(participant: NewParticipant) -> JSONResponse:

        if participants_col.find_one(filter={"email": participant.email}):
            return JSONResponse(
                content={
                    "message": "The email of the participant already exists!",
                },
                status_code=409,
            )

        insert_result: InsertOneResult = participants_col.insert_one(
            participant.model_dump(),
        )

        # if participant.team_name ?? handle accordingly
        # create_team(random=true)
        # else
        # ...

        # new_team = TeamsUtilities.create_team(
        #     str(insert_result.inserted_id),
        #     participant.team_name,
        # )
        # if not new_team:
        #     updated_team = TeamsUtilities.add_participant_to_team(
        #         participant.team_name,
        #         str(insert_result.inserted_id),
        #     )

        #     if not updated_team:
        #         raise Exception("Some Exception")

        # updated_team.team_name = paricipant.team_name

        #     TeamsUtilities.update_team_query(updated_team.model_dump())
        # else:
        #     TeamsUtilities.insert_team(team=new_team)

        return JSONResponse(
            content={"message": "The participant was successfully added!"},
            status_code=200,
        )
