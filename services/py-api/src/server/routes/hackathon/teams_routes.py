from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.dependency_wiring import HackathonManagementHandlersDep
from src.server.routes.routes_dependencies import is_auth, validate_obj_id
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse, AllTeamsResponse

teams_router = APIRouter(prefix="/hackathon/teams")


@teams_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_team(object_id: str, req_handler: HackathonManagementHandlersDep) -> Response:
    return await req_handler.delete_team(object_id)


@teams_router.get("/", status_code=200, responses={200: {"model": AllTeamsResponse}}, dependencies=[Depends(is_auth)])
async def get_all_teams(req_handler: HackathonManagementHandlersDep) -> Response:
    return await req_handler.get_all_teams()
