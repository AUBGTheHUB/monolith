from fastapi import APIRouter, Depends
from src.service.hackathon_service import HackathonService
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers
from src.server.routes.dependency_factory import _h_service
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse
from starlette.responses import Response
from src.server.routes.dependency_factory import is_auth, validate_obj_id


teams_router = APIRouter(prefix="/hackathon/teams")


def _handler(
    h_service: HackathonService = Depends(_h_service),
) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(h_service)


@teams_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_team(
    response: Response, object_id: str, handler: HackathonManagementHandlers = Depends(_handler)
) -> TeamDeletedResponse | ErrResponse:
    return await handler.delete_team(response, object_id)
