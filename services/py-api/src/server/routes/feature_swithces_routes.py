from fastapi import APIRouter, Depends

from src.server.handlers.feature_switch_handlers import FeatureSwitchHandlers
from src.server.routes.route_dependencies import is_auth
from src.server.schemas.response_schemas.schemas import ErrResponse, AllFeatureSwitchesResponse, FeatureSwitchResponse


def register_feature_switches_routes(http_handler: FeatureSwitchHandlers) -> APIRouter:
    """Registers all feature switches routes under a separate router, along with their respective handler funcs, and
    returns the router"""
    fs_router = APIRouter(prefix="/feature-switches")

    fs_router.add_api_route(
        path="/{feature}",
        methods=["GET"],
        endpoint=http_handler.get_feature_switch,
        responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}},
    )

    fs_router.add_api_route(
        path="",
        methods=["PATCH"],
        endpoint=http_handler.handle_feature_switch_update,
        responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
        dependencies=[Depends(is_auth)],
    )

    fs_router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=http_handler.get_all_feature_switches,
        responses={200: {"model": AllFeatureSwitchesResponse}},
    )

    return fs_router
