from os import environ
from typing import Annotated
from fastapi import Depends, HTTPException, Header, Path, Response
from fastapi.responses import JSONResponse
from src.database.db_manager import DB_MANAGER, FEATURE_SWITCH_COLLECTION, PARTICIPANTS_COLLECTION, TEAMS_COLLECTION
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.service.feature_switch_service import FeatureSwitchService
from src.service.hackathon_service import HackathonService
from bson import ObjectId
import json

from src.service.mail_service.hackathon_mail_service import HackathonMailService
from src.service.mail_service.mail_client import ResendMailClient

from starlette import status

from structlog.stdlib import get_logger

LOG = get_logger()

# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
# Dependency wiring


def _p_repo(db_manager: DB_MANAGER) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager, PARTICIPANTS_COLLECTION)

def _t_repo(db_manager: DB_MANAGER) -> TeamsRepository:
    return TeamsRepository(db_manager, TEAMS_COLLECTION)

def _tx_manager(db_manager: DB_MANAGER) -> TransactionManager:
    return TransactionManager(db_manager)


def _mail_service() -> HackathonMailService:
    # The client initialization could be made as a factory if more mailing clients are added
    return HackathonMailService(client=ResendMailClient())

def _fs_repo(db_manager: DB_MANAGER) -> FeatureSwitchRepository:
    return FeatureSwitchRepository(db_manager, FEATURE_SWITCH_COLLECTION)

def _fs_service(fs_repo: FeatureSwitchRepository = Depends(_fs_repo)) -> FeatureSwitchService:
    return FeatureSwitchService(fs_repo)

def _fs_handler(fs_service: FeatureSwitchService = Depends(_fs_service)) -> FeatureSwitchHandler:
    return FeatureSwitchHandler(fs_service)

def _h_service(
    p_repo: ParticipantsRepository = Depends(_p_repo),
    t_repo: TeamsRepository = Depends(_t_repo),
    fs_repo: FeatureSwitchRepository = Depends(_fs_repo),
    tx_manager: TransactionManager = Depends(_tx_manager),
    mail_service: HackathonMailService = Depends(_mail_service),
) -> HackathonService:
    return HackathonService(p_repo, t_repo, fs_repo, tx_manager, mail_service)


def is_auth(authorization: Annotated[str, Header()]) -> None:
    # This follows the dependency pattern that is provided to us by FastAPI
    # You can read more about it here:
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
    # I have exported this function on a separate dependencies file likes suggested in:
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
    if environ["ENV"] != "PROD":
        if not (
            authorization
            and authorization.startswith("Bearer ")
            and authorization[len("Bearer ") :] == environ["SECRET_AUTH_TOKEN"]
        ):
            raise HTTPException(detail="Unauthorized", status_code=401)
    else:
        # TODO: Implement JWT Bearer token authorization logic if we decide on an admin panel.
        #  For now every effort to access protected routes in a PROD env will not be authorized!
        raise HTTPException(detail="Unauthorized", status_code=401)


def validate_obj_id(object_id: Annotated[str, Path()]) -> None:
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)

async def registration_open(handler: FeatureSwitchHandler = Depends(_fs_handler)) -> None:
    response = await handler.handle_feature_switch(feature="isRegistrationOpen")

    decoded_response = json.loads(response.body.decode())

    if not decoded_response['feature']['state']:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration is closed"
        )