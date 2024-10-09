from fastapi import APIRouter

from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, ErrResponse

utility_router = APIRouter()


@utility_router.get("/ping", responses={200: {"model": PongResponse}})
async def ping() -> PongResponse | ErrResponse:
    return await UtilityHandlers.ping_service()
