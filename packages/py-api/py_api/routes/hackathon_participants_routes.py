from typing import Any, Dict

from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import PartcipantsController as c

router = APIRouter(prefix="/hackathon/participants")


@router.get("")
async def get_participants() -> JSONResponse:
    return c.get_all_participants()


@router.get("/{object_id}")
async def get_participant(object_id: str) -> JSONResponse:
    return c.get_specified_participant(object_id)


# @router.put("/{objectID}")
# async def update_participant(feature_switch: FeatureSwitch) -> Dict[str, Any]:
#     return c.update_switch(feature_switch)


# @router.delete("/{objectID}")
# async def delete_participant(switch_id: str) -> Dict[str, Any]:
#     return c.delete_switch(switch_id)
