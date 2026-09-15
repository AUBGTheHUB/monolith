from fastapi import APIRouter, Depends

from src.database.model.admin.hub_admin_model import Role
from src.server.handlers.admin.candidates_form.forms_handlers import CandidateFormsHandlers
from src.server.routes.route_dependencies import validate_obj_id
from src.server.schemas.response_schemas.admin.candidates_form.form_schemas import (
    CandidateFormResponse,
    CandidateFormsResponse,
)
from src.server.schemas.response_schemas.schemas import ErrResponse
from src.server.utility.role_checker import RoleChecker


def register_candidates_forms_router(http_handler: CandidateFormsHandlers) -> APIRouter:
    forms_router = APIRouter(prefix="/candidate-forms", tags=["forms"])

    forms_router.add_api_route(
        path="",
        endpoint=http_handler.get_all_forms,
        methods=["GET"],
        responses={200: {"model": CandidateFormsResponse}},
        dependencies=[Depends(RoleChecker([Role.BOARD]))],
    )
    forms_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.get_form,
        methods=["GET"],
        responses={
            200: {"model": CandidateFormResponse},
            400: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )
    forms_router.add_api_route(
        path="",
        endpoint=http_handler.create_form,
        methods=["POST"],
        responses={
            201: {"model": CandidateFormResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
    )
    forms_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.update_form,
        methods=["PATCH"],
        responses={
            200: {"model": CandidateFormResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )
    forms_router.add_api_route(
        path="/{object_id}",
        endpoint=http_handler.delete_form,
        methods=["DELETE"],
        responses={
            200: {"model": CandidateFormResponse},
            400: {"model": ErrResponse},
            401: {"model": ErrResponse},
            404: {"model": ErrResponse},
        },
        dependencies=[Depends(RoleChecker([Role.BOARD])), Depends(validate_obj_id)],
    )

    return forms_router
