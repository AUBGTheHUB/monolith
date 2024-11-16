from fastapi import Response, APIRouter, Depends

from src.database.db_manager import DB_MANAGER
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, ErrResponse
from src.utils import JwtUtility
from typing import Any 

utility_router = APIRouter()


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def create_utility_handler(db_manager: DB_MANAGER) -> UtilityHandlers:
    return UtilityHandlers(db_manager)


@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(
    response: Response, handler: UtilityHandlers = Depends(create_utility_handler)
) -> PongResponse | ErrResponse:
    return await handler.ping_services(response)

#Test encode function
@utility_router.get("/testjwt", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def testJWT() -> Any:
    return await JwtUtility.encode({"str":"fdsafsad"})