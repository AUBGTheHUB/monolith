from fastapi import APIRouter, Depends
from src.database.repository.teams_repository import TeamsRepository
from src.server.handlers.teams_handlers import TeamHandlers
from src.server.routes.dependency_factory import _t_repo
from src.server.schemas.response_schemas.schemas import ErrResponse, TeamDeletedResponse
from starlette.responses import Response
from src.server.routes.dependency_factory import is_auth, validate_obj_id


teams_router = APIRouter(prefix="/hackathon/teams")


def _handler(
    t_repo: TeamsRepository = Depends(_t_repo),
) -> TeamHandlers:
    return TeamHandlers(t_repo)


@teams_router.delete(
    "/{object_id}",
    status_code=200,
    responses={200: {"model": TeamDeletedResponse}, 404: {"model": ErrResponse}},
    dependencies=[Depends(is_auth), Depends(validate_obj_id)],
)
async def delete_team(
    response: Response, object_id: str, handler: TeamHandlers = Depends(_handler)
) -> TeamDeletedResponse | ErrResponse:
    return await handler.delete_team(response, object_id)
