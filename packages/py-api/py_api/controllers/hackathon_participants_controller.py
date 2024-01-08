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
        try:
            to_be_updated_participant = participants_col.find_one_and_update(
                {"_id": ObjectId(object_id)}, {
                    "$set": fields_to_be_updated,
                },
                return_document=True,
            )

        except (InvalidId, TypeError) as e:
            return JSONResponse(content={"message": "Invalid object_id format!"}, status_code=400)

        if not to_be_updated_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

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

        # A sample code snippet of how creation of team looks like
        # user_id = str(insert_result.inserted_id)
        # if participant.team_name:
        #     new_team = TeamsUtilities.create_team(
        #         user_id,
        #         participant.team_name,
        #     )
        #
        #     if new_team:
        #         TeamsUtilities.insert_team(team=new_team)
        #
        #     else:
        #         # Team with such name already exists
        #         updated_team = TeamsUtilities.add_participant_to_team(
        #             participant.team_name,
        #             user_id,
        #         )
        #
        #         if not updated_team:
        #             raise Exception("Some Exception")
        #
        #         TeamsUtilities.update_team_query(updated_team.model_dump())
        #
        # else:
        #     new_team = TeamsUtilities.create_team(
        #         user_id,
        #         generate_random_team=True
        #     )
        #     TeamsUtilities.insert_team(team=new_team)

        return JSONResponse(
            content={"message": "The participant was successfully added!"},
            status_code=200,
        )

    @classmethod
    def assign_random_team_to_participant(cls, object_id: str) -> JSONResponse:
        # Fetch the teams of type random
        avaliable_teams = []
        random_teams = TeamsUtilities.fetch_teams_by_condition(
            {"team_type": "random"},
        )

        # Find the teams which can accept a new participant
        for team in random_teams:
            if not TeamsUtilities.team_has_reach_max_cap(team):
                avaliable_teams.append(team)

        if avaliable_teams:
            # Since we are only creating new teams, when the max capacity of the existing ones is reached
            # We only need to check the last team of the List for the capacity(all the others should have max cap)
            next_avaliable_team = avaliable_teams[0]
            updated_avaliable_team = TeamsUtilities.add_participant_to_team(
                next_avaliable_team.team_name, object_id,
            )
            if updated_avaliable_team:
                cls.update_participant(
                    object_id, UpdateParticipant(
                        **{"team_name": updated_avaliable_team.team_name}
                    ),
                )
                TeamsUtilities.update_team_query(
                    updated_avaliable_team.model_dump(),
                )
                return JSONResponse(content=updated_avaliable_team.model_dump(), status_code=200)

        elif (TeamsUtilities.get_count_of_teams() < 15):
            # Create New Team and assign the participant to it
            newTeam = TeamsUtilities.create_team(
                object_id, TeamsUtilities.generate_random_team_name(), True,
            )
            if newTeam:
                cls.update_participant(
                    object_id, UpdateParticipant(
                        **{"team_name": newTeam.team_name}
                    ),
                )
                TeamsUtilities.insert_team(newTeam)
                return JSONResponse(content=newTeam.model_dump(), status_code=200)

        else:
            return JSONResponse(content={"message": "The maximum number of teams is reached."}, status_code=404)
