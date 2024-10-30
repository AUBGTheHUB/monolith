import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from structlog.stdlib import get_logger

from src.server.app_entrypoint import app

LOG = get_logger()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()
