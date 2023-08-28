from fastapi import APIRouter
from py_api.controllers.getting_logs_controller import GettingLogsController as c
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/logs")
async def get_logs() -> JSONResponse:
    return c.return_files()
