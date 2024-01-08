from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from py_api.controllers import ParticipantsController as p
from py_api.controllers import UtilityController as c

router = APIRouter()


@router.get('/health')
async def health() -> Dict[str, Any]:
    return c.get_health()


@router.get('/routes')
async def get_routes(request: Request) -> Dict[str, Dict[str, Any]]:
    return c.get_all_routes(request)


@router.get('/verify')
async def assign_team_to_participant() -> JSONResponse:
    return p.assign_random_team_to_participant('659bc16e326284810b83a72a')
