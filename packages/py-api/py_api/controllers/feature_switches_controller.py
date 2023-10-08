
from typing import Any, Dict, Final

from fastapi.responses import JSONResponse
from py_api.database import db
from py_api.models import FeatureSwitch
from py_api.utilities.parsers import has_prohibited_characters


class FeatureSwitchesController:

    fs_col = db.feature_switches

    COMMON_FS_NOT_FOUND_ERROR: Final = JSONResponse(
        content={
            "message": "No feature switch was found!",
        },
        status_code=404,
    )

    @classmethod
    def upsert_switch(cls, fs: FeatureSwitch) -> Dict[str, Any] | JSONResponse:
        dumped_fs = fs.model_dump()
        prohibited_chars = "'\";/:!@#$%\\[]^*()_-+{}=?.,§~`"

        if has_prohibited_characters(dumped_fs["switch_id"], prohibited_chars):
            return JSONResponse(content={"message": "Provided endpoint includes a prohibited character - {prohibited_chars}"}, status_code=400)

        document = cls.fs_col.find_one_and_update(
            {"switch_id": dumped_fs["switch_id"]}, {
                "$set": dumped_fs,
            }, upsert=True,
            projection={"_id": 0},
            return_document=True,
        )

        return {"document": document}

    @classmethod
    def get_switch(cls, switch_id: str) -> Dict[str, Any] | JSONResponse:
        projection = {"_id": 0}
        document = cls.fs_col.find_one(
            filter={"switch_id": switch_id}, projection=projection,
        )

        if not document:
            return cls.COMMON_FS_NOT_FOUND_ERROR

        return {"document": document}

    @classmethod
    def get_all_switches(cls) -> Dict[str, Any] | JSONResponse:
        projecetion = {"_id": 0}
        cursor = cls.fs_col.find({}, projecetion)

        if not cursor:
            return cls.COMMON_FS_NOT_FOUND_ERROR

        return {"documents": [doc for doc in cursor]}

    @classmethod
    def delete_switch(cls, switch_id: str) -> Dict[str, Any] | JSONResponse:
        document = cls.fs_col.find_one_and_delete({"switch_id": switch_id})

        if not document:
            return cls.COMMON_FS_NOT_FOUND_ERROR

        return {"message": "Feature switch was successfully deleted!"}
