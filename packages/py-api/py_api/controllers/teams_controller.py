import json

from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col, t_col
from py_api.models import UpdateTeam
from py_api.utilities.parsers import filter_none_values


class TeamsController:

    def fetch_teams() -> JSONResponse:
        teams = list(t_col.find())
        if not teams:
            return JSONResponse(content={"message": "No teams were found in db"}, status_code=404)

        for team in teams:
            team_name = team.get("team_name")
            participants = list(
                participants_col.find(
                    {"team_name": team_name}, {"_id": 1},
                ),
            )
            team["team_members"] = [
                str(participant["_id"])
                for participant in participants
            ]

        return JSONResponse(content={"teams": json.loads(dumps(teams))}, status_code=201)

    def get_team(object_id: str) -> JSONResponse:
        specified_team = t_col.find_one(filter={"_id": ObjectId(object_id)})

        if not specified_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_team))}, status_code=200)

    def delete_team(object_id: str) -> JSONResponse:
        delete_team = t_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not delete_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"message": json.loads(dumps(delete_team))}, status_code=200)

    def team_count() -> JSONResponse:
        count = t_col.count_documents({})

        if not count:
            return JSONResponse(content={"message": "No teams were found"}, status_code=404)

        return JSONResponse(content={"teams": count})

    def update_team(object_id: str, update_form: UpdateTeam) -> JSONResponse:
        fields_to_be_updated = filter_none_values(update_form)

        to_be_updated_participant = t_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": fields_to_be_updated,
            },
            return_document=True,
        )
        return JSONResponse(content={"teams": json.loads(dumps(to_be_updated_participant))}, status_code=200)
