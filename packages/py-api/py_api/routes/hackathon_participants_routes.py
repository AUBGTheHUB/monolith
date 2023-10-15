from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import PartcipantsController as c

router = APIRouter(prefix="/hackathon/participants")


@router.get("")
async def get_participants() -> JSONResponse:
    return c.get_all_participants()


# @router.get("/{objectID}")
# async def get_participant(objectID: str) -> JSONResponse:
#     return c.get_specific_participant(objectID)


# @router.put("/{objectID}")
# async def update_participant(feature_switch: FeatureSwitch) -> Dict[str, Any]:
#     return c.update_switch(feature_switch)


# @router.delete("/{objectID}")
# async def delete_participant(switch_id: str) -> Dict[str, Any]:
#     return c.delete_switch(switch_id)
