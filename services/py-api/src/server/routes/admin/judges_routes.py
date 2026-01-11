from fastapi import APIRouter, Depends

from src.server.handlers.admin.judges_handlers import JudgesHandlers
from src.server.routes.route_dependencies import is_auth


def register_judges_routes(http_handler: JudgesHandlers) -> APIRouter:
    judges_router = APIRouter(prefix="/judges", tags=["judges"])

    judges_router.add_api_route(
        "", endpoint=http_handler.get_all_judges, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    judges_router.add_api_route(
        "/{judge_id}", endpoint=http_handler.get_judge, methods=["GET"], dependencies=[Depends(is_auth)]
    )
    judges_router.add_api_route(
        "", endpoint=http_handler.create_judge, methods=["POST"], dependencies=[Depends(is_auth)]
    )
    judges_router.add_api_route(
        "/{judge_id}", endpoint=http_handler.update_judge, methods=["PATCH"], dependencies=[Depends(is_auth)]
    )
    judges_router.add_api_route(
        "/{judge_id}", endpoint=http_handler.delete_judge, methods=["DELETE"], dependencies=[Depends(is_auth)]
    )

    return judges_router
