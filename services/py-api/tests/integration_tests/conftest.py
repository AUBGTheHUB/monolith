import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.db_manager import PARTICIPANTS_COLLECTION, TEAMS_COLLECTION, DatabaseManager
from structlog.stdlib import get_logger

from src.server.app_entrypoint import app

LOG = get_logger()


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    LOG.debug("Opening Async Client")
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()


@pytest_asyncio.fixture(scope="session")
async def participant_repository() -> ParticipantsRepository:
    db_manager = DatabaseManager()
    p_repo = ParticipantsRepository(db_manager, PARTICIPANTS_COLLECTION)
    yield p_repo
    LOG.debug("Closing Database Connection")
    db_manager.close_all_connections()


@pytest_asyncio.fixture(scope="session")
async def team_repository() -> TeamsRepository:
    db_manager = DatabaseManager()
    t_repo = TeamsRepository(db_manager, TEAMS_COLLECTION)
    yield t_repo
    LOG.debug("Closing Database Connection")
    db_manager.close_all_connections()
