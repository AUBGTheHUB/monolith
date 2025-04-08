from unittest.mock import patch, AsyncMock

import pytest
from pymongo.errors import ConnectionFailure
from result import Err

from src.database.mongo.db_manager import MongoDatabaseManager
from src.utils import singleton


# https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request
@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    # Clear singleton instances before each test as we get inconsistent test results
    # Accessing private members of class like this is highly discouraged and is only possible as this is Python.
    # We do it only because this is an exceptional case. Using Singletons in unit tests could be tricky :(
    singleton._instances.clear()


@pytest.fixture
def db_manager() -> MongoDatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value.admin.command = AsyncMock(return_value={"ok": 1})
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return MongoDatabaseManager()


@pytest.fixture
def db_manager_err_operation() -> MongoDatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value.admin.command = AsyncMock(side_effect=ConnectionFailure("Test err"))
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return MongoDatabaseManager()


@pytest.fixture
def db_manager_none_client() -> MongoDatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value = None
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return MongoDatabaseManager()


@pytest.mark.asyncio
async def test_async_ping_db_success(db_manager: MongoDatabaseManager) -> None:
    result = await db_manager.async_ping_db()
    assert result is None


@pytest.mark.asyncio
async def test_async_ping_db_err(db_manager_err_operation: MongoDatabaseManager) -> None:
    result = await db_manager_err_operation.async_ping_db()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_close_all_connections_success(db_manager: MongoDatabaseManager) -> None:
    result = db_manager.close_all_connections()
    assert result is None


@pytest.mark.asyncio
async def test_close_all_connections_err(db_manager_none_client: MongoDatabaseManager) -> None:
    result = db_manager_none_client.close_all_connections()
    isinstance(result, Err)
