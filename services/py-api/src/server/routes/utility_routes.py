from fastapi import Response, APIRouter, Depends

from src.database.db_manager import DB_MANAGER
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, ErrResponse
from src.utils import JwtUtility
from typing import Any 

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
utility_router = APIRouter()


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def create_utility_handler(db_manager: DB_MANAGER) -> UtilityHandlers:
    return UtilityHandlers(db_manager)


# https://fastapi.tiangolo.com/advanced/additional-responses/
@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(
    response: Response, handler: UtilityHandlers = Depends(create_utility_handler)
) -> PongResponse | ErrResponse:
    return await handler.ping_services(response)