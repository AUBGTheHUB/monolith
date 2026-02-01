from typing import cast

import pytest
from result import Err

from src.database.mongo.db_manager import MongoDatabaseManager
from src.server.handlers.utility_handlers import UtilityHandlers
from src.server.schemas.response_schemas.schemas import Response, PongResponse, ErrResponse
from tests.unit_tests.conftest import MongoDbManagerMock


@pytest.fixture
async def handler(mongo_db_manager_mock: MongoDbManagerMock) -> UtilityHandlers:
    return UtilityHandlers(cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_ping_handler(mongo_db_manager_mock: MongoDbManagerMock, handler: UtilityHandlers) -> None:

    # Given
    # Mock that async_ping_db return no error
    mongo_db_manager_mock.async_ping_db.return_value = None

    # When
    result = await handler.ping_services()

    # Then
    assert isinstance(result, Response)
    assert isinstance(result.response_model, PongResponse)


@pytest.mark.asyncio
async def test_ping_handler_error(mongo_db_manager_mock: MongoDbManagerMock, handler: UtilityHandlers) -> None:

    # Given
    # Mock that async_ping_db return no error
    mongo_db_manager_mock.async_ping_db.return_value = Err("Test error")

    # When
    result = await handler.ping_services()

    # Then
    assert isinstance(result, Response)
    assert result.response_model == ErrResponse(error="Database not available!")
