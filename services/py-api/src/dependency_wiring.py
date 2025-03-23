"""Here we do our Dependency Wiring via the FastAPI Dependency Injection system. Under the hood when a new APIRouter is
defined, FastAPI goes through each route in the given router and starts building the object dependency graph. After all
dependencies and their dependencies have been gathered, FastAPI starts traversing the graph and resolving them one by
one. This resolution is achieved by internally calling  ``fastapi.Depends``. which calls the passed callable, returning
an instance ready to be used.

A graphical representation of this graph looks something like this:

```
                          Repositories -> DbManagers -> DbClients
                         /
Routes -> Handlers -> Services -> OtherServices -> OtherComponents
                         \
                          MailServices ->  MailClients
```

* Note: -> Means accepts (e.g. Routes -> Handlers, means Routes accept handlers as dependencies)

To learn more about FastAPI Dependency Injection system:
# https://fastapi.tiangolo.com/tutorial/dependencies/
# https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies
"""

from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.database.db_clients import mongo_db_client_provider
from src.database.mongo.db_manager import (
    FEATURE_SWITCH_COLLECTION,
    PARTICIPANTS_COLLECTION,
    TEAMS_COLLECTION,
    MongoDatabaseManager,
)
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.service.feature_switch_service import FeatureSwitchService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_service import HackathonService
from src.service.hackathon.participants_registration_service import ParticipantRegistrationService
from src.service.hackathon.participants_verification_service import ParticipantVerificationService
from src.service.jwt_utils.codec import JwtUtility
from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.mail_clients.mail_client_factory import mail_client_factory, MailClients

# ===============================
# Database layer wiring start
# ===============================

# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
_MongoDbClientDep = Annotated[AsyncIOMotorClient, Depends(mongo_db_client_provider)]


def _get_mongo_db_manager(client: _MongoDbClientDep) -> MongoDatabaseManager:
    return MongoDatabaseManager(client=client)


_MongoDbManagerDep = Annotated[MongoDatabaseManager, Depends(_get_mongo_db_manager)]


def _get_mongo_tx_manager(client: _MongoDbClientDep) -> MongoTransactionManager:
    return MongoTransactionManager(client=client)


_MongoTxManagerDep = Annotated[MongoTransactionManager, Depends(_get_mongo_db_manager)]


def _get_participants_repo(
    db_manager: _MongoDbManagerDep, collection_name: str = PARTICIPANTS_COLLECTION
) -> ParticipantsRepository:
    return ParticipantsRepository(db_manager=db_manager, collection_name=collection_name)


_ParticipantsRepoDep = Annotated[ParticipantsRepository, Depends(_get_participants_repo)]


def _get_teams_repo(db_manager: _MongoDbManagerDep, collection_name: str = TEAMS_COLLECTION) -> TeamsRepository:
    return TeamsRepository(db_manager=db_manager, collection_name=collection_name)


_TeamsRepoDep = Annotated[TeamsRepository, Depends(_get_participants_repo)]


def _get_fs_repo(
    db_manager: _MongoDbManagerDep, collection_name: str = FEATURE_SWITCH_COLLECTION
) -> FeatureSwitchRepository:
    return FeatureSwitchRepository(db_manager=db_manager, collection_name=collection_name)


_FeatureSwitchRepoDep = Annotated[FeatureSwitchRepository, Depends(_get_participants_repo)]

# ===============================
# Database layer wiring end
# ===============================


# ===============================
# Service layer wiring start
# ===============================

# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#shortcut
_JwtUtilityDep = Annotated[JwtUtility, Depends()]


def _get_mail_client() -> MailClient:
    # Could be changed with another client if needed
    return mail_client_factory(mail_client_type=MailClients.RESEND)


_MailClientDep = Annotated[MailClient, Depends(_get_mail_client)]


def _get_hackathon_mail_service(client: _MailClientDep) -> HackathonMailService:
    return HackathonMailService(client=client)


_HackathonMailServiceDep = Annotated[HackathonMailService, Depends(_get_hackathon_mail_service)]


def _get_hackathon_service(
    p_repo: _ParticipantsRepoDep,
    t_repo: _TeamsRepoDep,
    fs_repo: _FeatureSwitchRepoDep,
    tx_manager: _MongoTxManagerDep,
    mail_service: _HackathonMailServiceDep,
    jwt_utility: _JwtUtilityDep,
) -> HackathonService:
    return HackathonService(
        participant_repo=p_repo,
        team_repo=t_repo,
        feature_switch_repo=fs_repo,
        tx_manager=tx_manager,
        mail_service=mail_service,
        jwt_utility=jwt_utility,
    )


_HackathonServiceDep = Annotated[HackathonService, Depends(_get_hackathon_service)]


def _get_participant_reg_service(
    hackathon_service: _HackathonServiceDep, jwt_utility: _JwtUtilityDep
) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(hackathon_service=hackathon_service, jwt_utility=jwt_utility)


_ParticipantsRegServiceDep = Annotated[ParticipantRegistrationService, Depends(_get_participant_reg_service)]


def _get_participant_verification_servicer(hackathon_service: _HackathonServiceDep) -> ParticipantVerificationService:
    return ParticipantVerificationService(hackathon_service)


_ParticipantVerificationServiceDep = Annotated[
    ParticipantVerificationService, Depends(_get_participant_verification_servicer)
]


def _get_feature_switch_service(repository: _FeatureSwitchRepoDep) -> FeatureSwitchService:
    return FeatureSwitchService(repository)


_FeatureSwitchServiceDep = Annotated[FeatureSwitchService, Depends(_get_feature_switch_service)]


# ===============================
# Service layer wiring end
# ===============================

# ===============================
# Handlers layer wiring start
# ===============================

# These Dependencies are public as they are imported in the `routes/routes_dependencies.py`
# There for every handler we should create a wrapper function which returns the already created instance.
# For more info, check the docs in the `routes/routes_dependencies.py` file.


def _get_feature_switch_handlers(service: _FeatureSwitchServiceDep) -> FeatureSwitchHandler:
    return FeatureSwitchHandler(service=service)


FeatureSwitchHandlerDep = Annotated[FeatureSwitchHandler, Depends(_get_feature_switch_handlers)]
"""A FastAPI dependency for getting a FeatureSwitchHandler instance"""


def _get_hackathon_management_handlers(service: _HackathonServiceDep) -> HackathonManagementHandlers:
    return HackathonManagementHandlers(service=service)


HackathonManagementHandlersDep = Annotated[HackathonManagementHandlers, Depends(_get_hackathon_management_handlers)]
"""A FastAPI dependency for getting a HackathonManagementHandlers instance"""


def _get_participant_handlers(service: _ParticipantsRegServiceDep) -> ParticipantHandlers:
    return ParticipantHandlers(service=service)


ParticipantHandlersDep = Annotated[ParticipantHandlers, Depends(_get_participant_handlers)]
"""A FastAPI dependency for getting a ParticipantHandlers instance"""


def _get_utility_handlers(db_manger: _MongoDbManagerDep) -> UtilityHandlers:
    return UtilityHandlers(db_manger=db_manger)


UtilityHandlersDep = Annotated[UtilityHandlers, Depends(_get_utility_handlers)]
"""A FastAPI dependency for getting a UtilityHandlers instance"""


def _get_verification_handlers(
    service: _ParticipantVerificationServiceDep, jwt_utility: _JwtUtilityDep
) -> VerificationHandlers:
    return VerificationHandlers(service=service, jwt_utility=jwt_utility)


VerificationHandlersDep = Annotated[VerificationHandlers, Depends(_get_verification_handlers)]
"""A FastAPI dependency for getting a VerificationHandlers instance"""

# ===============================
# Handlers layer wiring end
# ===============================
