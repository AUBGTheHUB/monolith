import json

from bson.json_util import dumps
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

        # projecetion = {"_id": 0}
        # cursor = cls.participants_col.find({}, projecetion)

        # if not cursor:
        #     return cls.COMMON_PARTICIPANTS_NOT_FOUND_ERROR

        # return {"participants": [doc for doc in cursor]}

    # @classmethod
    # def get_specific_participant(cls, objectID: ObjectId) -> JSONResponse:
