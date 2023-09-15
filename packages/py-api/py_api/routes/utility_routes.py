from typing import Any, Dict

from fastapi import APIRouter, Request
from py_api.controllers import UtilityController as c

router = APIRouter()


@router.get('/health')
async def health() -> Dict[str, Any]:
    return c.get_health()


@router.get('/routes')
async def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
    return c.get_all_routes(request)
