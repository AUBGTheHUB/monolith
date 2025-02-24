from fastapi import APIRouter, Depends

from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.routes.routes_dependencies import (
    get_utility_handlers_handlers,
    get_feature_switch_handlers,
    is_auth,
    get_hackathon_management_handlers,
)
from src.server.schemas.request_schemas.schemas import FeatureSwitchUpdateBody
from src.server.schemas.response_schemas.schemas import (
    FeatureSwitchResponse,
    PongResponse,
    ErrResponse,
    AllFeatureSwitchesResponse,
    RegistrationClosedSuccessfullyResponse,
    Response,
)

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
utility_router = APIRouter()


# https://fastapi.tiangolo.com/advanced/additional-responses/
@utility_router.get("/ping", responses={200: {"model": PongResponse}, 503: {"model": ErrResponse}})
async def ping(handler: UtilityHandlers = Depends(get_utility_handlers_handlers)) -> Response:
    return await handler.ping_services()


@utility_router.get(
    "/feature-switches/{feature}", responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}}
)
async def get_feature_switch(
    feature: str, handler: FeatureSwitchHandler = Depends(get_feature_switch_handlers)
) -> Response:
    return await handler.get_feature_switch(feature=feature)


@utility_router.patch(
    "/feature-switches",
    status_code=200,
    responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
    dependencies=[Depends(is_auth)],
)
async def update_feature_switch(
    request_body: FeatureSwitchUpdateBody, handler: FeatureSwitchHandler = Depends(get_feature_switch_handlers)
) -> Response:
    return await handler.handle_feature_switch_update(name=request_body.name, state=request_body.state)


@utility_router.get("/feature-switches", responses={200: {"model": AllFeatureSwitchesResponse}})
async def get_all_feature_switches(handler: FeatureSwitchHandler = Depends(get_feature_switch_handlers)) -> Response:
    return await handler.get_all_feature_switches()


@utility_router.post(
    "/hackathon/close-registration",
    responses={200: {"model": RegistrationClosedSuccessfullyResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth)],
)
async def close_hackathon_registration(
    handler: HackathonManagementHandlers = Depends(get_hackathon_management_handlers),
) -> Response:
    return await handler.close_registration()
