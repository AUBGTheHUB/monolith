from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.database.db_manager import DB_MANAGER
from src.database.query_manager import QueryManager
from src.database.repositories.participants_repository import ParticipantsRepository
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import ParticipantResponse, ErrResponse

participants_router = APIRouter(prefix="/hackathon/participants")
COLLECTION = "participants"


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def _create_query_manager(db_manager: DB_MANAGER) -> QueryManager:
    return QueryManager(db_manager, COLLECTION)


def _create_repository(query_manager: QueryManager = Depends(_create_query_manager)) -> ParticipantsRepository:
    return ParticipantsRepository(query_manager)


def _create_handler(repository: ParticipantsRepository = Depends(_create_repository)) -> ParticipantHandlers:
    return ParticipantHandlers(repository)


@participants_router.post("")
async def create_participant(
    response: Response, req_body: ParticipantRequestBody, handler: ParticipantHandlers = Depends(_create_handler)
) -> ParticipantResponse | ErrResponse:
    # TODO: Add docs
    return await handler.create_participant(response, req_body)
