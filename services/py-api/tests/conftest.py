from datetime import datetime, timedelta
from typing import Tuple

import pytest
import pytest_asyncio
from unittest.mock import Mock, MagicMock, AsyncMock

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
    db_manager = Mock(spec=DatabaseManager)
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    db_manager.client = AsyncMock()
    db_manager.get_collection.return_value = AsyncMock()

    return db_manager


@pytest.fixture
def response_mock() -> MagicMock:
    return MagicMock(spec=Response)


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)
