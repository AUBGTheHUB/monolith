from fastapi import Response, APIRouter, Depends

from src.database.db_manager import DB_MANAGER
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.routes.dependency_factory import _fs_repo
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse, PongResponse, ErrResponse
from src.service.feature_switch_service import FeatureSwitchService

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
utility_router = APIRouter()


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def create_utility_handler(db_manager: DB_MANAGER) -> UtilityHandlers:
    return UtilityHandlers(db_manager)

def _fs_service(fs_repo: FeatureSwitchRepository = Depends(_fs_repo)): 
    return FeatureSwitchService(fs_repo)

def _fs_handler(fs_service: FeatureSwitchService = Depends(_fs_service)): 
    return FeatureSwitchHandler(fs_service)


# https://fastapi.tiangolo.com/advanced/additional-responses/
@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(handler: UtilityHandlers = Depends(create_utility_handler)) -> Response:
    return await handler.ping_services()

@utility_router.get("/feature-switch", 
                    responses={200: {"model": FeatureSwitchResponse}, 409: {"model": ErrResponse}})
async def registration_open_status(feature: str, handler: FeatureSwitchHandler = Depends(_fs_handler)) -> Response:
    return await handler.handle_feature_switch(feature=feature)
