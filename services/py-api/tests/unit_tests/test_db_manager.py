from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError

from src.database.db_manager import DatabaseManager


@pytest.fixture
def setup_database_manager() -> DatabaseManager:
    # We Patch the call in order to avoid real connection to the database during initialization
    with patch("src.database.db_manager.AsyncIOMotorClient"):
        return DatabaseManager()


def test_close_all_connections_not_initialized(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = None
    result = db_manager.close_all_connections()
    # Adding a custom message if the assertion fails, for better debugging
    assert result.is_err(), "Should return an error if client is not initialized"
    assert result.err_value == "The database client is not initialized!"


def test_close_all_connections_success(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = MagicMock()
    db_manager.close_all_connections()
    # MagicMock objects create all attributes and methods as you access them
    db_manager._client.close.assert_called_once()


@pytest.mark.asyncio
async def test_async_ping_db_success(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = MagicMock()
    db_manager._client.admin.command = AsyncMock()
    await db_manager.async_ping_db()
    db_manager._client.admin.command.assert_called_once_with("ping")


@pytest.mark.asyncio
async def test_async_ping_db_connection_failure(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = MagicMock()
    db_manager._client.admin.command = AsyncMock(side_effect=ConnectionFailure)
    result = await db_manager.async_ping_db()
    assert result.is_err(), "Should return an error if there is a connection failure"
    assert result.err_value == "Database is unavailable!"


@pytest.mark.asyncio
async def test_async_ping_db_operation_failure(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = MagicMock()
    db_manager._client.admin.command = AsyncMock(side_effect=OperationFailure("Operation failed"))
    result = await db_manager.async_ping_db()
    assert result.is_err(), "Should return an error if there is an operation failure"
    assert result.err_value == "Database authentication failed!"


@pytest.mark.asyncio
async def test_async_ping_db_configuration_error(setup_database_manager: DatabaseManager) -> None:
    db_manager = setup_database_manager
    db_manager._client = MagicMock()
    db_manager._client.admin.command = AsyncMock(side_effect=ConfigurationError)
    result = await db_manager.async_ping_db()
    assert result.is_err(), "Should return an error if there is a configuration error"
    assert result.err_value == "Database authentication failed!"
