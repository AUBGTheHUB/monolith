from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers.logs_controller import LogsController as c

router = APIRouter()


@router.get("/logs")
async def get_logs() -> JSONResponse:
    return c.get_log_file()
