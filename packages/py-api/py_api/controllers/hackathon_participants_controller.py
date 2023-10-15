from typing import Any, Dict, Final

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col


class PartcipantsController:

    COMMON_PARTICIPANTS_NOT_FOUND_ERROR: Final = JSONResponse(
        content={
            "message": "No participants were found!",
        },
        status_code=404,
    )

    @classmethod
    def get_all_participants(cls) -> JSONResponse:
        cursor = participants_col.find({})
        list_cur = list(cursor)

        if not cursor:
            return cls.COMMON_PARTICIPANTS_NOT_FOUND_ERROR

        else:
            return JSONResponse(content=dumps(list_cur), status_code=200)

        # projecetion = {"_id": 0}
        # cursor = cls.participants_col.find({}, projecetion)

        # if not cursor:
        #     return cls.COMMON_PARTICIPANTS_NOT_FOUND_ERROR

        # return {"participants": [doc for doc in cursor]}

    # @classmethod
    # def get_specific_participant(cls, objectID: ObjectId) -> JSONResponse:
