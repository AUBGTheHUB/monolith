import json

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col
from py_api.functionality.hackathon.teams.teams_utility_functions import TeamsUtilities
from py_api.models.hackathon_teams_models import HackathonTeam, UpdateTeam


class TeamsController:

    @classmethod
    def fetch_teams(cls) -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(
                content={"message": "No teams were found in db"},
                status_code=404,
            )

        return JSONResponse(
            content={"teams": json.loads(dumps(teams))},
            status_code=200,
        )

    @classmethod
    def get_team(cls, object_id: str) -> JSONResponse:
        specified_team = TeamsUtilities.fetch_team(team_id=object_id)
        if not specified_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(
            content={"team": specified_team.model_dump()},
            status_code=200,
        )

    @staticmethod
    def delete_team(object_id: str) -> JSONResponse:
        delete_team = t_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not delete_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(
            content={"message": json.loads(dumps(delete_team))},
            status_code=200,
        )

    @staticmethod
    def team_count() -> JSONResponse:
        count = TeamsUtilities.get_count_of_teams()

        if count == 0:
            return JSONResponse(
                content={"message": "No teams were found"},
                status_code=404,
            )

        return JSONResponse(content={"teams": count})

    @classmethod
    def update_team(
        cls, object_id: str,
        team_payload: UpdateTeam | HackathonTeam,
    ) -> JSONResponse:
        updated_team = TeamsUtilities.update_team_query(
            team_payload=team_payload.model_dump(), object_id=object_id,
        )

        if not updated_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(content={"team": updated_team}, status_code=200)
