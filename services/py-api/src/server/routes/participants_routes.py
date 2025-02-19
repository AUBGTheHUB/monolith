from typing import Union
from fastapi import APIRouter, Depends, BackgroundTasks
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers
from src.server.routes.dependency_factory import _h_service, registration_open, _p_handler
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
    ParticipantDeletedResponse,
    Response,
)
from src.service.hackathon_service import HackathonService
from src.server.routes.dependency_factory import is_auth, validate_obj_id

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
participants_router = APIRouter(prefix="/hackathon/participants")


def _h_handler(
    h_service: HackathonService = Depends(_h_service),
) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(h_service)


# https://fastapi.tiangolo.com/advanced/additional-responses/
# https://fastapi.tiangolo.com/tutorial/background-tasks/#dependency-injection
@participants_router.post(
    "",
    status_code=201,
    responses={201: {"model": ParticipantRegisteredResponse}, 409: {"model": ErrResponse}},
    dependencies=[Depends(registration_open)],
)
async def create_participant(
    participant_request_body: ParticipantRequestBody,
    background_tasks: BackgroundTasks,
    jwt_token: Union[str, None] = None,
    participant_handler: ParticipantHandlers = Depends(_p_handler),
) -> Response:
    return await participant_handler.create_participant(participant_request_body, background_tasks, jwt_token)


@participants_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": ParticipantDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_participant(object_id: str, handler: HackathonManagementHandlers = Depends(_h_handler)) -> Response:
    return await handler.delete_participant(object_id)
