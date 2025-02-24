from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.routes.routes_dependencies import is_auth, validate_obj_id, get_hackathon_management_handlers
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse, AllTeamsResponse

teams_router = APIRouter(prefix="/hackathon/teams")


@teams_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_team(
    object_id: str, handler: HackathonManagementHandlers = Depends(get_hackathon_management_handlers)
) -> Response:
    return await handler.delete_team(object_id)


@teams_router.get("/", status_code=200, responses={200: {"model": AllTeamsResponse}}, dependencies=[Depends(is_auth)])
async def get_all_teams(handler: HackathonManagementHandlers = Depends(get_hackathon_management_handlers)) -> Response:
    return await handler.get_all_teams()
