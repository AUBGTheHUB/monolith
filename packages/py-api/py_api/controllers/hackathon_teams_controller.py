import json
import random
import string
from typing import Literal

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col
from py_api.models import UpdateTeam
from py_api.utilities.parsers import filter_none_values


class TeamsController:
    @classmethod
    def create_team(cls, team_name: str, user_id: str) -> Literal[True] | Literal[False]:
        """Creates a new team in the db with one team member.
        This method should be used when a new participant is created.

        Examples:

        >>>result = participants_col.insert_one(participant_form_dump)
        >>>TeamsController.create_team(participant_form_dump["team_name"], str(result.inserted_id))

        Returns:
             - True if the team was created
             - False if such team exists
        """

        team_type = "normal"

        if not team_name:
            # Generates a random string of 8 characters if team_name is ""
            # which means that the participant is random
            team_name = ''.join(
                random.choice(string.ascii_letters)
                for _ in range(8)
            )
            team_type = "random"

        team = t_col.find_one(filter={"team_name": team_name})

        if not team:
            t_col.insert_one({
                "team_name": team_name,
                "team_type": team_type,
                "team_members": [user_id],
            })
            return True

        return False

    @classmethod
    def append_team_members(cls, team_name: str, user_id: str) -> Literal[True] | Literal[False]:
        team = t_col.find_one(filter={"team_name": team_name})

        # If this method is used to a register participants via the sharable link,
        # the next 2 lines might be redundant
        if not team:
            return False

        team_members = team.get("team_members")
        team_members.append(user_id)

        t_col.update_one(
            {"team_name": team_name}, {
                "$set": {"team_members": team_members},
            }, )

        return True

    @staticmethod
    def fetch_teams() -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(content={"message": "No teams were found in db"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(teams))}, status_code=200)

    @staticmethod
    def get_team(object_id: str) -> JSONResponse:
        specified_team = t_col.find_one(filter={"_id": ObjectId(object_id)})

        if not specified_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_team))}, status_code=200)

    @staticmethod
    def delete_team(object_id: str) -> JSONResponse:
        delete_team = t_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not delete_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"message": json.loads(dumps(delete_team))}, status_code=200)

    @staticmethod
    def team_count() -> JSONResponse:
        count = t_col.count_documents({})

        if not count:
            return JSONResponse(content={"message": "No teams were found"}, status_code=404)

        return JSONResponse(content={"teams": count})

    @staticmethod
    def update_team(object_id: str, update_table_model: UpdateTeam) -> JSONResponse:
        fields_to_be_updated = filter_none_values(update_table_model)

        to_be_updated_team = t_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": fields_to_be_updated,
            },
            return_document=True,
        )

        if not to_be_updated_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(to_be_updated_team))}, status_code=200)
