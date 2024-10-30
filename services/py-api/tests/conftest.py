from datetime import datetime, timedelta
from typing import Tuple

import pytest
import pytest_asyncio
from unittest.mock import Mock, MagicMock, AsyncMock

from httpx import AsyncClient, ASGITransport
from starlette.responses import Response
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.app_entrypoint import app
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody

LOG = get_logger()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()


@pytest.fixture
def db_manager_mock() -> Mock:
    db_manager = Mock(spec=DatabaseManager)
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    db_manager.client = AsyncMock()
    db_manager.get_collection.return_value = AsyncMock()

    return db_manager


@pytest.fixture
def participant_repo_mock() -> Mock:
    participant_repo = Mock(spec=ParticipantsRepository)

    participant_repo.fetch_by_id = AsyncMock()
    participant_repo.fetch_all = AsyncMock()
    participant_repo.update = AsyncMock()
    participant_repo.create = AsyncMock()
    participant_repo.delete = AsyncMock()

    return participant_repo


@pytest.fixture
def team_repo_mock() -> Mock:
    team_repo = Mock(spec=TeamsRepository)

    team_repo.fetch_by_id = AsyncMock()
    team_repo.fetch_all = AsyncMock()
    team_repo.update = AsyncMock()
    team_repo.create = AsyncMock()
    team_repo.delete = AsyncMock()

    return team_repo


@pytest.fixture
def tx_manager_mock() -> Mock:
    tx_manager = Mock(spec=TransactionManager)
    tx_manager.with_transaction = AsyncMock()

    return tx_manager


@pytest.fixture
def mock_input_data() -> ParticipantRequestBody:
    return ParticipantRequestBody(name="Test User", email="test@example.com", team_name="Test Team", is_admin=True)


@pytest.fixture
def response_mock() -> MagicMock:
    return MagicMock(spec=Response)


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)
