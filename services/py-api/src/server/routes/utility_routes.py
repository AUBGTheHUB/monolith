from fastapi import APIRouter, Depends

from src.dependency_wiring import HackathonManagementHandlersDep, FeatureSwitchHandlerDep, UtilityHandlersDep
from src.server.routes.routes_dependencies import (
    is_auth,
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
async def ping(req_handler: UtilityHandlersDep) -> Response:
    return await req_handler.ping_services()


@utility_router.get(
    "/feature-switches/{feature}", responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}}
)
async def get_feature_switch(feature: str, req_handler: FeatureSwitchHandlerDep) -> Response:
    return await req_handler.get_feature_switch(feature=feature)


@utility_router.patch(
    "/feature-switches",
    status_code=200,
    responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
    dependencies=[Depends(is_auth)],
)
async def update_feature_switch(
    request_body: FeatureSwitchUpdateBody, req_handler: FeatureSwitchHandlerDep
) -> Response:
    return await req_handler.handle_feature_switch_update(name=request_body.name, state=request_body.state)


@utility_router.get("/feature-switches", responses={200: {"model": AllFeatureSwitchesResponse}})
async def get_all_feature_switches(req_handler: FeatureSwitchHandlerDep) -> Response:
    return await req_handler.get_all_feature_switches()


@utility_router.post(
    "/hackathon/close-registration",
    responses={200: {"model": RegistrationClosedSuccessfullyResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth)],
)
async def close_hackathon_registration(req_handler: HackathonManagementHandlersDep) -> Response:
    return await req_handler.close_registration()
