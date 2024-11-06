from unittest.mock import patch, AsyncMock

import pytest
from pymongo.errors import ConnectionFailure
from result import Err

from src.database.db_manager import DatabaseManager


@pytest.fixture
def db_manager() -> DatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value.admin.command = AsyncMock(return_value={"ok": 1})
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return DatabaseManager()


@pytest.fixture
def db_manager_err_operation() -> DatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value.admin.command = AsyncMock(side_effect=ConnectionFailure("Test err"))
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return DatabaseManager()


@pytest.fixture
def db_manager_none_client() -> DatabaseManager:
    with patch("src.database.db_manager.AsyncIOMotorClient") as mock_client:
        mock_client.return_value = None
        # https://stackoverflow.com/questions/42565304/is-it-possible-to-ping-mongodb-from-pymongo
        with patch("src.database.db_manager.environ", {"DATABASE_URL": "mongodb+srv://test_url"}):
            return DatabaseManager()


@pytest.mark.asyncio
async def test_async_ping_db_success(db_manager: DatabaseManager) -> None:
    result = await db_manager.async_ping_db()
    assert result is None


@pytest.mark.asyncio
async def test_async_ping_db_err(db_manager_err_operation: DatabaseManager) -> None:
    result = await db_manager_err_operation.async_ping_db()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_close_all_connections_success(db_manager: DatabaseManager) -> None:
    result = db_manager.close_all_connections()
    assert result is None


@pytest.mark.asyncio
async def test_close_all_connections_err(db_manager_none_client: DatabaseManager) -> None:
    result = db_manager_none_client.close_all_connections()
    assert isinstance(result, Err)
