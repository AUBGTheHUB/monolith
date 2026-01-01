from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from structlog.stdlib import get_logger

from src.database.db_clients import mongo_db_client_provider
from src.database.mongo.db_manager import (
    MongoDatabaseManager,
    PARTICIPANTS_COLLECTION,
    TEAMS_COLLECTION,
    FEATURE_SWITCH_COLLECTION,
    DB_NAME,
)
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.http_handlers import HttpHandlersContainer
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.middleware.middleware import register_all_exception_handlers, register_all_middlewares
from src.server.routes.routes import Routes
from src.service.feature_switch_service import FeatureSwitchService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_service import HackathonService
from src.service.hackathon.participants_registration_service import ParticipantRegistrationService
from src.service.hackathon.participants_verification_service import ParticipantVerificationService
from src.service.jwt_utils.codec import JwtUtility
from src.service.mail_service.mail_clients.mail_client_factory import mail_client_factory, MailClients

LOG = get_logger()


def _ping_db(mongo_client: AsyncIOMotorClient) -> None:
    """
    This method is used only on application startup.
    Raises:
        ConnectionFailure
        OperationFailure
        ConfigurationError
    """

    try:
        LOG.debug("Pinging MongoDB...")
        mongo_client.get_database(name=DB_NAME).command("ping")

    except ConnectionFailure as cf:
        LOG.exception("Pinging db failed due to err", error=cf)
        raise cf

    except (OperationFailure, ConfigurationError) as err:
        LOG.exception("Pinging db failed due to err", error=err)
        raise err
    else:
        LOG.debug("Pong")

    return None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    To learn more about lifespan events, visit:
    https://fastapi.tiangolo.com/advanced/events/#lifespan
    https://www.starlette.io/lifespan/
    https://asgi.readthedocs.io/en/latest/specs/lifespan.html

    To learn more about context managers, visit:
    https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager
    """
    # Open a connection to Mongo
    db_client = mongo_db_client_provider()
    _ping_db(db_client)

    # @asynccontextmanager makes the function an Async context manager. We need the yield as this decorator must be
    # applied to an asynchronous generator function. https://docs.python.org/3/glossary.html#term-asynchronous-generator
    #
    # Under the hood the whole application is wrapped withing this context manager. On context manager entry
    # (__aenter__) `anext` is called, which runs the code until it hits the yield statement. When the yield statement
    # is hit we yield (return) back control to the code inside the guard (our main application).
    #
    # On context manager exit (__aexit__) `anext` is called again, which executes the code after the yield statement.
    # As the server runs continuously (in a while loop) we most commonly exit the context manager on:
    # SIGINT signal  # Unix signal 2. Sent by Ctrl+C.
    # SIGTERM signal,  # Unix signal 15. Sent by `kill <pid>`.

    yield

    # Close the opened connections towards MongoDB
    db_client.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, root_path="/api/v3")

    """
    Note:
    The dependencies below are essentially singletons, as they are created only once (on app creation) and then then
    reused throughout the app's lifetime.
    If you need to create a dependency that creates a new instance on demand (for example on every request) you should
    use `FastAPI.Depends`.
    See https://fastapi.tiangolo.com/tutorial/dependencies/
    """

    # Database layer dependency wiring
    db_manager = MongoDatabaseManager(client=mongo_db_client_provider())
    tx_manager = MongoTransactionManager(client=mongo_db_client_provider())
    participants_repo = ParticipantsRepository(db_manager=db_manager, collection_name=PARTICIPANTS_COLLECTION)
    teams_repo = TeamsRepository(db_manager=db_manager, collection_name=TEAMS_COLLECTION)
    fs_repo = FeatureSwitchRepository(db_manager=db_manager, collection_name=FEATURE_SWITCH_COLLECTION)

    # Store FeatureSwitchRepository in app.state for access in route dependencies
    # https://www.starlette.io/applications/#storing-state-on-the-app-instance
    app.state.fs_repo = fs_repo

    # Service layer wiring
    jwt_utility = JwtUtility()
    mail_client = mail_client_factory(mail_client_type=MailClients.RESEND)
    hackathon_mail_service = HackathonMailService(client=mail_client)
    hackathon_service = HackathonService(
        participants_repo=participants_repo,
        teams_repo=teams_repo,
        feature_switch_repo=fs_repo,
        tx_manager=tx_manager,
        mail_service=hackathon_mail_service,
        jwt_utility=jwt_utility,
    )
    participants_reg_service = ParticipantRegistrationService(
        hackathon_service=hackathon_service, jwt_utility=jwt_utility
    )
    participants_verification_service = ParticipantVerificationService(hackathon_service=hackathon_service)
    fs_service = FeatureSwitchService(repository=fs_repo)

    # Handlers layer wiring
    http_handlers = HttpHandlersContainer(
        utility_handlers=UtilityHandlers(db_manager=db_manager),
        fs_handlers=FeatureSwitchHandler(service=fs_service),
        hackathon_management_handlers=HackathonManagementHandlers(service=hackathon_service),
        participant_handlers=ParticipantHandlers(service=participants_reg_service),
        verification_handlers=VerificationHandlers(service=participants_verification_service, jwt_utility=jwt_utility),
    )

    Routes.register_routes(app.router, http_handlers)

    # Register exception handlers and middlewares explicitly
    register_all_exception_handlers(app)
    register_all_middlewares(app)

    return app
