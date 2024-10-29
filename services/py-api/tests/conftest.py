import pytest
import pytest_asyncio
from unittest.mock import Mock, MagicMock

from httpx import AsyncClient, ASGITransport
from starlette.responses import Response
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.server.app_entrypoint import app

LOG = get_logger()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()


@pytest.fixture
def db_manager_mock() -> Mock:
    return Mock(spec=DatabaseManager)


@pytest.fixture
def response_mock() -> MagicMock:
    return MagicMock(spec=Response)
