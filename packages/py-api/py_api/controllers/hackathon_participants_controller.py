import json

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col


class PartcipantsController:

    @classmethod
    def get_all_participants(cls) -> JSONResponse:
        participants = list(participants_col.find())

        if not participants:
            return JSONResponse(content={"message": "No participants were found!"}, status_code=404)

        # the dumps funtion from bson.json_util returns a string
        return JSONResponse(content={"participants": json.loads(dumps(participants))}, status_code=200)

    @classmethod
    def get_specified_participant(cls, object_id: str) -> JSONResponse:
        specified_participant = participants_col.find_one(
            filter={"_id": ObjectId(object_id)},
        )

        if not specified_participant:
            return JSONResponse(content={"message": "Specified participant not found!"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_participant))}, status_code=200)
