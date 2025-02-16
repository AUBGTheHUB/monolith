from typing import cast

import pytest
from pymongo.errors import ConnectionFailure
from result import Err
from starlette import status

from src.database.db_managers import MongoDatabaseManager
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, Response, ErrResponse
from tests.unit_tests.conftest import MongoDbManagerMock


@pytest.fixture
def utility_handler(mongo_db_manager_mock: MongoDbManagerMock) -> UtilityHandlers:
    return UtilityHandlers(db_manger=cast(MongoDatabaseManager, mongo_db_manager_mock))


@pytest.mark.asyncio
async def test_ping_handler(utility_handler: UtilityHandlers, mongo_db_manager_mock: MongoDbManagerMock) -> None:
    # Given that async_ping_db return no error
    mongo_db_manager_mock.async_ping_db.return_value = None

    # When we call the handler
    result = await utility_handler.ping_services()

    # Then we should get a 200 response
    assert isinstance(result, Response)
    assert isinstance(result.response_model, PongResponse)
    assert result.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_ping_handler_error(utility_handler: UtilityHandlers, mongo_db_manager_mock: MongoDbManagerMock) -> None:
    # Given that async_ping_db returns an error
    mongo_db_manager_mock.async_ping_db.return_value = Err(ConnectionFailure())

    # When we call the handler
    result = await utility_handler.ping_services()

    # Then we should get a 503 response
    assert isinstance(result, Response)
    assert result.response_model == ErrResponse(error="Database not available!")
    assert result.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
