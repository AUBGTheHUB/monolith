from fastapi import APIRouter, Depends

from src.server.handlers.admin.judges_handlers import JudgesHandlers
from src.server.routes.route_dependencies import is_authorized, validate_obj_id
from src.server.schemas.response_schemas.admin.judge_schemas import JudgesResponse, JudgeResponse
from src.server.schemas.response_schemas.schemas import ErrResponse


def register_judges_routes(http_handler: JudgesHandlers) -> APIRouter:
    judges_router = APIRouter(prefix="/judges", tags=["judges"])

    judges_router.add_api_route(
        "", endpoint=http_handler.get_all_judges, methods=["GET"], responses={200: {"model": JudgesResponse}}
    )

    judges_router.add_api_route(
        "/{judge_id}",
        endpoint=http_handler.get_judge,
        methods=["GET"],
        responses={200: {"model": JudgeResponse}, 400: {"model": ErrResponse}, 404: {"model": ErrResponse}},
        dependencies=[Depends(validate_obj_id)],
    )

    judges_router.add_api_route(
        "",
        endpoint=http_handler.create_judge,
        methods=["POST"],
        responses={
            201: {"model": JudgeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized)],
    )

    judges_router.add_api_route(
        "/{judge_id}",
        endpoint=http_handler.update_judge,
        methods=["PATCH"],
        responses={
            200: {"model": JudgeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized)],
    )

    judges_router.add_api_route(
        "/{judge_id}",
        endpoint=http_handler.delete_judge,
        methods=["DELETE"],
        responses={
            200: {"model": JudgeResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(is_authorized)],
    )

    return judges_router
