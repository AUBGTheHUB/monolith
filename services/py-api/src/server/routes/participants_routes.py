from typing import Union

from fastapi import APIRouter, Depends, BackgroundTasks

from src.server.routes.path_operation_decorators import is_auth, validate_obj_id
from src.server.handlers.hackathon_handlers import HackathonManagementHandlersDep
from src.server.handlers.participants_handlers import ParticipantHandlersDep
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
    ParticipantDeletedResponse,
    Response,
)

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
participants_router = APIRouter(prefix="/hackathon/participants")


# https://fastapi.tiangolo.com/advanced/additional-responses/
@participants_router.post(
    "", status_code=201, responses={201: {"model": ParticipantRegisteredResponse}, 409: {"model": ErrResponse}}
)
async def create_participant(
    participant_request_body: ParticipantRequestBody,
    background_tasks: BackgroundTasks,
    handler: ParticipantHandlersDep,
    jwt_token: Union[str, None] = None,
) -> Response:
    """
    Args:
        participant_request_body: https://fastapi.tiangolo.com/tutorial/body/
        background_tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/#dependency-injection
        handler: https://fastapi.tiangolo.com/tutorial/dependencies/
        jwt_token: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

    Returns:
        A JSON response
    """
    return await handler.create_participant(participant_request_body, background_tasks, jwt_token)


@participants_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": ParticipantDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_participant(object_id: str, handler: HackathonManagementHandlersDep) -> Response:
    return await handler.delete_participant(object_id)
