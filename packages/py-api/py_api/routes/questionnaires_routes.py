from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from py_api.controllers import QuestionnairesController as c

router = APIRouter(prefix='/questionnaires')


@router.get("/csv/{dep}")
async def get_csv(dep) -> StreamingResponse:  # type: ignore
    return c.get_csv(dep)
