from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.server.routes.path_operation_decorators import is_auth, validate_obj_id
from src.server.handlers.hackathon_handlers import HackathonManagementHandlersDep
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse

teams_router = APIRouter(prefix="/hackathon/teams")


@teams_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_team(object_id: str, handler: HackathonManagementHandlersDep) -> Response:
    return await handler.delete_team(object_id)
