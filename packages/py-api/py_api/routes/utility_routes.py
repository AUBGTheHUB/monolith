from logging import getLogger
from typing import Any, Dict

from fastapi import APIRouter, Request
from py_api.controllers import UtilitiesController as c

router = APIRouter()
logger = getLogger("health")


@router.get('/health')
async def health(request: Request) -> Dict[str, Any]:
    result: Dict[str, Any] = c.health(request)
    return result


@router.get('/routes')
async def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
    return c.get_routes(request)
