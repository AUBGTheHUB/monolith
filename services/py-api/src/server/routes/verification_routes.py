from typing import Any
from fastapi import APIRouter, Response, Depends

from src.database.db_manager import DB_MANAGER, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.handlers.verification_handlers import VerificationHandlers
from src.service.hackathon_service import HackathonService
from src.service.verification_service import VerificationService


verification_router = APIRouter(prefix="/hackathon/participants/verify")


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


def _v_service(
    h_service: HackathonService = Depends(_h_service),
) -> VerificationService:
    return VerificationService(h_service)


def _handler(v_service: VerificationService = Depends(_v_service)) -> VerificationHandlers:
    return VerificationHandlers(v_service)


@verification_router.get("", status_code=200)
async def verify_participant(
    response: Response, jwt_token: str, _handler: VerificationHandlers = Depends(_handler)
) -> Any:
    return await _handler.verifyParticipant(response=response, jwt_token=jwt_token)
