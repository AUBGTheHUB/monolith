from typing import Any, Dict, Final

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
        for column in participants_col.find():
            return JSONResponse(content={column}, status_code=200)
        return JSONResponse(content={"test": "test"}, status_code=200)
        # projecetion = {"_id": 0}
        # cursor = cls.participants_col.find({}, projecetion)

        # if not cursor:
        #     return cls.COMMON_PARTICIPANTS_NOT_FOUND_ERROR

        # return {"participants": [doc for doc in cursor]}
