from typing import Union

from fastapi import APIRouter, Depends, BackgroundTasks

from src.dependency_wiring import ParticipantHandlersDep, HackathonManagementHandlersDep
from src.server.routes.routes_dependencies import (
    is_auth,
    validate_obj_id,
    registration_open,
)
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
# https://fastapi.tiangolo.com/tutorial/background-tasks/#dependency-injection
@participants_router.post(
    "",
    status_code=201,
    responses={201: {"model": ParticipantRegisteredResponse}, 409: {"model": ErrResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(registration_open)],
)
async def create_participant(
    participant_request_body: ParticipantRequestBody,
    background_tasks: BackgroundTasks,
    req_handler: ParticipantHandlersDep,
    jwt_token: Union[str, None] = None,
) -> Response:
    return await req_handler.create_participant(participant_request_body, background_tasks, jwt_token)


@participants_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": ParticipantDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_participant(object_id: str, req_handler: HackathonManagementHandlersDep) -> Response:
    return await req_handler.delete_participant(object_id)
