from fastapi import APIRouter, Depends

from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.routes.route_dependencies import is_auth
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse, ErrResponse, AllFeatureSwitchesResponse


def register_feature_switches_routes(main_router: APIRouter, http_handler: FeatureSwitchHandler) -> None:
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

    # Bind the fs_router (request multiplexer) to the main router
    main_router.include_router(fs_router)
