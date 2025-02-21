from fastapi import Response, APIRouter, Depends

from src.database.db_manager import DB_MANAGER
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.routes.dependency_factory import _fs_handler, is_auth
from src.server.schemas.request_schemas.schemas import FeatureSwitchUpdateBody
from src.server.schemas.response_schemas.schemas import (
    FeatureSwitchResponse,
    PongResponse,
    ErrResponse,
    AllFeatureSwitchesResponse,
)

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
utility_router = APIRouter()


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def create_utility_handler(db_manager: DB_MANAGER) -> UtilityHandlers:
    return UtilityHandlers(db_manager)


# https://fastapi.tiangolo.com/advanced/additional-responses/
@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(handler: UtilityHandlers = Depends(create_utility_handler)) -> Response:
    return await handler.ping_services()


@utility_router.get(
    "/feature-switches/{feature}", responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}}
)
async def get_feature_switch(feature: str, handler: FeatureSwitchHandler = Depends(_fs_handler)) -> Response:
    return await handler.handle_feature_switch(feature=feature)


@utility_router.patch(
    "/feature-switches",
    status_code=200,
    responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
    dependencies=[Depends(is_auth)],
)
async def update_feature_switch(
    request_body: FeatureSwitchUpdateBody, handler: FeatureSwitchHandler = Depends(_fs_handler)
) -> Response:
    return await handler.handle_feature_switch_update(name=request_body.name, state=request_body.state)


@utility_router.get("/feature-switches", responses={200: {"model": AllFeatureSwitchesResponse}})
async def get_all_feature_switches(handler: FeatureSwitchHandler = Depends(_fs_handler)) -> Response:
    return await handler.handle_all_feature_switches()
