from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.database.db_manager import DB_MANAGER, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import AdminParticipantRegisteredResponse, ErrResponse
from src.service.participants_service import ParticipantService

participants_router = APIRouter(prefix="/hackathon/participants")


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
# Dependency wiring


def _p_repo(db_manager: DB_MANAGER) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager, PARTICIPANTS_COLLECTION)


def _t_repo(db_manager: DB_MANAGER) -> TeamsRepository:
    return TeamsRepository(db_manager, TEAMS_COLLECTION)


def _tx_manager(db_manager: DB_MANAGER) -> TransactionManager:
    return TransactionManager(db_manager)


def _service(
    p_repo: ParticipantsRepository = Depends(_p_repo),
    t_repo: TeamsRepository = Depends(_t_repo),
    tx_manager: TransactionManager = Depends(_tx_manager),
) -> ParticipantService:
    return ParticipantService(p_repo, t_repo, tx_manager)


def _handler(service: ParticipantService = Depends(_service)) -> ParticipantHandlers:
    return ParticipantHandlers(service)


@participants_router.post(
    "", responses={201: {"model": AdminParticipantRegisteredResponse}, 409: {"model": ErrResponse}}
)
async def create_participant(
    response: Response, input_data: ParticipantRequestBody, handler: ParticipantHandlers = Depends(_handler)
) -> AdminParticipantRegisteredResponse | ErrResponse:
    return await handler.create_participant(response, input_data)
