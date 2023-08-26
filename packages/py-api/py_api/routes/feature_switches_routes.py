from typing import Any, Dict

from fastapi import APIRouter
from py_api.controllers import FeatureSwitchesController as c
from py_api.models import FeatureSwitch

router = APIRouter(prefix="/fswitches")


@router.get("")
async def get_switches() -> Dict[str, Any]:
    return c.get_all_switches()


@router.get("/{switch_id}")
async def get_switch(switch_id: str) -> Dict[str, Any]:
    return c.get_switch(switch_id)


@router.put("")
async def upsert_switch(feature_switch: FeatureSwitch) -> Dict[str, Any]:
    return c.upsert_switch(feature_switch)


@router.delete("/{switch_id}")
async def delete_switch(switch_id: str) -> Dict[str, Any]:
    return c.delete_switch(switch_id)
