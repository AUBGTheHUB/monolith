from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.database.db_manager import DB_MANAGER, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import ParticipantRegisteredInTeamResponse, ErrResponse
from src.service.hackathon_service import HackathonService
from src.service.participants_registration_service import ParticipantRegistrationService

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
participants_router = APIRouter(prefix="/hackathon/participants")


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
# Dependency wiring


def _p_repo(db_manager: DB_MANAGER) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager, PARTICIPANTS_COLLECTION)


def _t_repo(db_manager: DB_MANAGER) -> TeamsRepository:
    return TeamsRepository(db_manager, TEAMS_COLLECTION)


def _tx_manager(db_manager: DB_MANAGER) -> TransactionManager:
    return TransactionManager(db_manager)


def _h_service(
    p_repo: ParticipantsRepository = Depends(_p_repo),
    t_repo: TeamsRepository = Depends(_t_repo),
    tx_manager: TransactionManager = Depends(_tx_manager),
) -> HackathonService:
    return HackathonService(p_repo, t_repo, tx_manager)


def _p_service(
    h_service: HackathonService = Depends(_h_service),
    tx_manager: TransactionManager = Depends(_tx_manager),
) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(h_service, tx_manager)


def _handler(p_service: ParticipantRegistrationService = Depends(_p_service)) -> ParticipantHandlers:
    return ParticipantHandlers(p_service)


# https://fastapi.tiangolo.com/advanced/additional-responses/
@participants_router.post(
    "", status_code=201, responses={201: {"model": ParticipantRegisteredInTeamResponse}, 409: {"model": ErrResponse}}
)
async def create_participant(
    response: Response, input_data: ParticipantRequestBody, handler: ParticipantHandlers = Depends(_handler)
) -> ParticipantRegisteredInTeamResponse | ErrResponse:
    return await handler.create_participant(response, input_data)
