import json
from typing import Dict

from bson.json_util import dumps
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col


class TeamsController:

    def fetch_teams() -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(content={"message": "No teams were found in db"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(teams))}, status_code=201)
