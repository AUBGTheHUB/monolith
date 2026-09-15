from fastapi import APIRouter, Depends

from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.admin.candidates_form.questions_handlers import QuestionsHandlers
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.admin.candidates_form.question_schemas import (
    QuestionResponse,
    QuestionsResponse,
)
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.utility.role_checker import RoleChecker


def register_candidates_form_questions_router(http_handler: QuestionsHandlers) -> APIRouter:
    questions_router = APIRouter(prefix="/questions", tags=["questions"])

    questions_router.add_api_route(
        path="", endpoint=http_handler.get_all_questions, methods=["GET"], responses={200: {"model": QuestionsResponse}}
    )
    questions_router.add_api_route(
        path="/type/{question_type}",
        endpoint=http_handler.get_by_type,
        methods=["GET"],
        responses={200: {"model": QuestionsResponse}},
    )
    questions_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.get_question,
        methods=["GET"],
        responses={
            200: {"model": QuestionResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )
    questions_router.add_api_route(
        path="",
        endpoint=http_handler.create_question,
        methods=["POST"],
        responses={
            201: {"model": QuestionResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )
    questions_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.update_question,
        methods=["PATCH"],
        responses={
            200: {"model": QuestionResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )
    questions_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.delete_question,
        methods=["DELETE"],
        responses={
            200: {"model": QuestionResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )

    return questions_router
