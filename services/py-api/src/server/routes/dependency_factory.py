from fastapi import Depends
from src.database.db_manager import DB_MANAGER, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.service.hackathon_service import HackathonService


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
