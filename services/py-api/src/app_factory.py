from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from structlog.stdlib import get_logger

from src.database.db_clients import mongo_db_client_provider
from src.database.mongo.db_manager import MongoDatabaseManager, DB_NAME
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.server.exception_handler import ExceptionHandlers
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.http_handlers import HttpHandlersContainer
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.handlers.admin.admin_handlers import AdminHandlers
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.database.repository.admin.judges_repository import JudgesRepository
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.service.admin.sponsors_service import SponsorsService
from src.service.admin.mentors_service import MentorsService
from src.service.admin.judges_service import JudgesService
from src.service.admin.hub_members_service import HubMembersService
from src.service.admin.past_events_service import PastEventsService
from src.server.middleware.middleware import Middlewares
from src.server.routes.routes import Routes
from src.service.feature_switches.feature_switch_service import FeatureSwitchService
from src.service.hackathon.admin_team_service import AdminTeamService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.registration_service import RegistrationService
from src.service.hackathon.verification_service import VerificationService
from src.service.hackathon.team_service import TeamService
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
    participants_repo = ParticipantsRepository(db_manager=db_manager)
    teams_repo = TeamsRepository(db_manager=db_manager)
    fs_repo = FeatureSwitchRepository(db_manager=db_manager)
    sponsors_repo = SponsorsRepository(db_manager=db_manager)
    mentors_repo = MentorsRepository(db_manager=db_manager)
    judges_repo = JudgesRepository(db_manager=db_manager)
    hub_members_repo = HubMembersRepository(db_manager=db_manager)
    past_events_repo = PastEventsRepository(db_manager=db_manager)

    # Store FeatureSwitchRepository in app.state for access in route dependencies
    # https://www.starlette.io/applications/#storing-state-on-the-app-instance
    app.state.fs_repo = fs_repo

    # Service layer wiring
    jwt_utility = JwtUtility()
    mail_client = mail_client_factory(mail_client_type=MailClients.RESEND)
    hackathon_mail_service = HackathonMailService(client=mail_client)
    participant_service = ParticipantService(
        participants_repo=participants_repo,
        teams_repo=teams_repo,
        jwt_utility=jwt_utility,
        hackathon_mail_service=hackathon_mail_service,
    )
    team_service = TeamService(
        teams_repo=teams_repo,
        participant_service=participant_service,
        participant_repo=participants_repo,
        tx_manager=tx_manager,
    )
    admin_team_service = AdminTeamService(
        teams_repo=teams_repo, participant_repo=participants_repo, tx_manager=tx_manager
    )
    hackathon_utility_service = HackathonUtilityService(
        participants_repo=participants_repo,
        teams_repo=teams_repo,
        team_service=team_service,
        feature_switch_repo=fs_repo,
    )

    registration_service = RegistrationService(
        participant_service=participant_service,
        hackathon_utility_service=hackathon_utility_service,
        jwt_utility=jwt_utility,
        team_service=team_service,
        admin_team_service=admin_team_service,
    )
    verification_service = VerificationService(
        hackathon_utility_service=hackathon_utility_service,
        team_service=team_service,
        admin_team_service=admin_team_service,
        participant_service=participant_service,
    )
    fs_service = FeatureSwitchService(repository=fs_repo)
    sponsors_service = SponsorsService(repo=sponsors_repo)
    mentors_service = MentorsService(repo=mentors_repo)
    judges_service = JudgesService(repo=judges_repo)
    hub_members_service = HubMembersService(repo=hub_members_repo)
    past_events_service = PastEventsService(repo=past_events_repo)

    # Handlers layer wiring
    http_handlers = HttpHandlersContainer(
        utility_handlers=UtilityHandlers(db_manager=db_manager),
        fs_handlers=FeatureSwitchHandler(service=fs_service),
        hackathon_management_handlers=HackathonManagementHandlers(
            hackathon_utility_service=hackathon_utility_service,
            participant_service=participant_service,
            team_service=team_service,
        ),
        participant_handlers=ParticipantHandlers(service=registration_service),
        verification_handlers=VerificationHandlers(service=verification_service, jwt_utility=jwt_utility),
        admin_handlers=AdminHandlers(
            sponsors_service=sponsors_service,
            mentors_service=mentors_service,
            judges_service=judges_service,
            hub_members_service=hub_members_service,
            past_events_service=past_events_service,
        ),
    )

    Routes.register_routes(app.router, http_handlers)
    ExceptionHandlers.register_exception_handlers(app)
    Middlewares.register_middlewares(app)

    return app
