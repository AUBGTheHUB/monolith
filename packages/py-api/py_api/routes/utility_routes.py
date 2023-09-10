from logging import getLogger
from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from py_api.controllers import UtilityController as c
from py_api.utilities.memory import get_current_memory_usage_in_mbs

router = APIRouter()


@router.get('/health')
async def health() -> Dict[str, Any]:
    return c.get_health()


@router.get('/routes')
async def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
    return c.get_all_routes(request)
