from typing import Union
from fastapi import APIRouter, Depends, BackgroundTasks
from result import is_err
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers

from src.server.routes.dependency_factory import _h_service
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import (
    ParticipantRegisteredResponse,
    ErrResponse,
    ParticipantDeletedResponse,
    Response,
)
from src.service.feature_switch_service import FeatureSwitchService
from src.service.hackathon_service import HackathonService
from src.service.participants_registration_service import ParticipantRegistrationService
from src.server.routes.dependency_factory import is_auth, validate_obj_id
from starlette import status

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
participants_router = APIRouter(prefix="/hackathon/participants")


def _p_reg_service(h_service: HackathonService = Depends(_h_service)) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(h_service)

def _fs_service(h_service: HackathonService = Depends(_h_service),) -> FeatureSwitchService:
    return FeatureSwitchService(h_service._fs_repo)


def _p_handler(p_service: ParticipantRegistrationService = Depends(_p_reg_service)) -> ParticipantHandlers:
    return ParticipantHandlers(p_service)


def _h_handler(
    h_service: HackathonService = Depends(_h_service),
) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(h_service)

def _fs_handler(fs_service: FeatureSwitchService = Depends(_fs_service)) -> FeatureSwitchHandler:
    return FeatureSwitchHandler(fs_service)


# https://fastapi.tiangolo.com/advanced/additional-responses/
@participants_router.post(
    "", status_code=201, responses={201: {"model": ParticipantRegisteredResponse}, 409: {"model": ErrResponse}}
)
async def create_participant(
    participant_request_body: ParticipantRequestBody,
    background_tasks: BackgroundTasks,
    jwt_token: Union[str, None] = None,
    participant_handler: ParticipantHandlers = Depends(_p_handler),
    feature_switch_handler: FeatureSwitchHandler = Depends(_fs_handler),
) -> Response:
    
    registration_status_result = await feature_switch_handler.handle_feature_switch("isRegistrationOpen")
    
    if is_err(registration_status_result):
        return Response(
            ErrResponse(error=registration_status_result.err_value),
            status_code=status.HTTP_409_CONFLICT,
        )

    return await participant_handler.create_participant(participant_request_body, jwt_token)


@participants_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": ParticipantDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_participant(object_id: str, handler: HackathonManagementHandlers = Depends(_h_handler)) -> Response:
    return await handler.delete_participant(object_id)
