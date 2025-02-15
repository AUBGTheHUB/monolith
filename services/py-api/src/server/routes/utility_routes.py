from fastapi import Response, APIRouter

from src.server.handlers.utility_hanlders import UtilityHandlersDep
from src.server.schemas.response_schemas.schemas import PongResponse, ErrResponse

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
utility_router = APIRouter()


# https://fastapi.tiangolo.com/advanced/additional-responses/
@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(handler: UtilityHandlersDep) -> Response:
    return await handler.ping_services()
