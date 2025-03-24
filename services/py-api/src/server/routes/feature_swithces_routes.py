from fastapi import APIRouter, Depends

from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.routes.routes_dependencies import is_auth
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse, ErrResponse, AllFeatureSwitchesResponse


def register_feature_switches_routes(router: APIRouter, http_handler: FeatureSwitchHandler) -> None:
    router.add_api_route(
        path="/feature-switches/{feature}",
        methods=["GET"],
        endpoint=http_handler.get_feature_switch,
        responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}},
    )

    router.add_api_route(
        path="/feature-switches",
        methods=["PATCH"],
        endpoint=http_handler.handle_feature_switch_update,
        responses={200: {"model": FeatureSwitchResponse}, 404: {"model": ErrResponse}, 400: {"model": ErrResponse}},
        status_code=200,
        dependencies=[Depends(is_auth)],
    )

    router.add_api_route(
        path="/feature-switches",
        methods=["GET"],
        endpoint=http_handler.get_feature_switch,
        responses={200: {"model": AllFeatureSwitchesResponse}},
    )
