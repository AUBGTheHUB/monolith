from fastapi import Response, APIRouter

from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.response_schemas.schemas import PongResponse, ErrResponse

utility_router = APIRouter()


@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(response: Response) -> PongResponse | ErrResponse:
    return await UtilityHandlers.ping_services(response)
