from typing import cast

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from src.database.mongo.db_manager import MongoDatabaseManager
from tests.unit_tests.conftest import MotorDbClientMock, MotorDatabaseMock


@pytest.fixture
def db_manager(motor_db_client_mock: MotorDbClientMock) -> MongoDatabaseManager:
    return MongoDatabaseManager(client=cast(AsyncIOMotorClient, motor_db_client_mock))


@pytest.fixture
def db_manager_none_client() -> MongoDatabaseManager:
    return MongoDatabaseManager(client=None)


@pytest.mark.asyncio
async def test_async_ping_db_success(db_manager: MongoDatabaseManager, motor_database_mock: MotorDatabaseMock) -> None:
    # Given command("ping) has passed successfully
    motor_database_mock.command.return_value = {"ok": 1}

    # When we ping the database
    err = await db_manager.async_ping_db()

    # Then no error is returned
    assert err is None


@pytest.mark.asyncio
async def test_async_ping_db_err(db_manager: MongoDatabaseManager, motor_database_mock: MotorDatabaseMock) -> None:
    # Given command("ping) has raised a ConnectionFailure exception
    motor_database_mock.command.side_effect = ConnectionFailure("Test err")

    # When we ping the database
    err = await db_manager.async_ping_db()

    # Then an Err(ConnectionFailure) should be returned
    assert err is not None
    assert isinstance(err.err_value, ConnectionFailure)


@pytest.mark.asyncio
async def test_close_all_connections_success(db_manager: MongoDatabaseManager) -> None:
    err = db_manager.close_all_connections()
    assert err is None


@pytest.mark.asyncio
async def test_close_all_connections_err(db_manager_none_client: MongoDatabaseManager) -> None:
    err = db_manager_none_client.close_all_connections()
    assert err is not None
