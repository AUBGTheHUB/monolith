from os import environ
from typing import Annotated
from starlette import status
from fastapi import Depends, HTTPException, Header, Path
from src.database.db_manager import DB_MANAGER, FEATURE_SWITCH_COLLECTION, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.handlers.verification_handlers import VerificationHandlers
from src.service.feature_switch_service import FeatureSwitchService
from src.service.hackathon_service import HackathonService
from bson import ObjectId
from result import is_err

from src.service.mail_service.hackathon_mail_service import HackathonMailService
from src.service.mail_service.mail_client import ResendMailClient
from src.service.participants_registration_service import ParticipantRegistrationService
from src.service.participants_verification_service import ParticipantVerificationService

# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
# Dependency wiring

REGISTRATION_FEATURE_SWITCH = "RegSwitch"


def _p_repo(db_manager: DB_MANAGER) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager, PARTICIPANTS_COLLECTION)


def _t_repo(db_manager: DB_MANAGER) -> TeamsRepository:
    return TeamsRepository(db_manager, TEAMS_COLLECTION)


def _fs_repo(db_manager: DB_MANAGER) -> FeatureSwitchRepository:
    return FeatureSwitchRepository(db_manager, FEATURE_SWITCH_COLLECTION)


def _tx_manager(db_manager: DB_MANAGER) -> TransactionManager:
    return TransactionManager(db_manager)


def _mail_service() -> HackathonMailService:
    # The client initialization could be made as a factory if more mailing clients are added
    return HackathonMailService(client=ResendMailClient())


def _fs_service(fs_repo: FeatureSwitchRepository = Depends(_fs_repo)) -> FeatureSwitchService:
    return FeatureSwitchService(fs_repo)


def _h_service(
    p_repo: ParticipantsRepository = Depends(_p_repo),
    t_repo: TeamsRepository = Depends(_t_repo),
    fs_repo: FeatureSwitchRepository = Depends(_fs_repo),
    tx_manager: TransactionManager = Depends(_tx_manager),
    mail_service: HackathonMailService = Depends(_mail_service),
) -> HackathonService:
    return HackathonService(p_repo, t_repo, fs_repo, tx_manager, mail_service)


def _p_verify_service(h_service: HackathonService = Depends(_h_service)) -> ParticipantVerificationService:
    return ParticipantVerificationService(h_service)


def _p_reg_service(h_service: HackathonService = Depends(_h_service)) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(h_service)


# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
def _utility_handler(db_manager: DB_MANAGER) -> UtilityHandlers:
    return UtilityHandlers(db_manager)


def _p_handler(p_service: ParticipantRegistrationService = Depends(_p_reg_service)) -> ParticipantHandlers:
    return ParticipantHandlers(p_service)


def _h_handler(
    h_service: HackathonService = Depends(_h_service),
) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(h_service)


def _p_verify_handler(
    p_verify_service: ParticipantVerificationService = Depends(_p_verify_service),
) -> VerificationHandlers:
    return VerificationHandlers(p_verify_service)


def _fs_handler(fs_service: FeatureSwitchService = Depends(_fs_service)) -> FeatureSwitchHandler:
    return FeatureSwitchHandler(fs_service)


def is_auth(authorization: Annotated[str, Header()]) -> None:
    # This follows the dependency pattern that is provided to us by FastAPI
    # You can read more about it here:
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
    # I have exported this function on a separate dependencies file likes suggested in:
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
    # TODO: When the admin panel is implemented, the secret auth toke env variable should be removed as tokens
    #  will be automatically rotated
    if not (
        authorization
        and authorization.startswith("Bearer ")
        and authorization[len("Bearer ") :] == environ["SECRET_AUTH_TOKEN"]
    ):
        raise HTTPException(detail="Unauthorized", status_code=401)


def validate_obj_id(object_id: Annotated[str, Path()]) -> None:
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)


async def registration_open(fs_service: FeatureSwitchService = Depends(_fs_service)) -> None:

    is_registration_open = await fs_service.check_feature_switch(feature=REGISTRATION_FEATURE_SWITCH)

    if is_err(is_registration_open):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occured")

    if is_registration_open.ok_value.state is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")
