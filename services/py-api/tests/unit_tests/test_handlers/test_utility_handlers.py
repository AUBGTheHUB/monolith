from unittest.mock import Mock

import pytest
from result import Err

from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, Response, ErrResponse


@pytest.mark.asyncio
async def test_ping_handler(db_manager_mock: Mock) -> None:
    # Mock that async_ping_db return no error
    db_manager_mock.async_ping_db.return_value = None
    handler = UtilityHandlers(db_manager_mock)

    result = await handler.ping_services()

    assert isinstance(result, Response)
    assert isinstance(result.response_model, PongResponse)


@pytest.mark.asyncio
async def test_ping_handler_error(db_manager_mock: Mock) -> None:
    # Mock that async_ping_db return no error
    db_manager_mock.async_ping_db.return_value = Err("Test error")
    handler = UtilityHandlers(db_manager_mock)

    result = await handler.ping_services()

    assert isinstance(result, Response)
    assert result.response_model == ErrResponse(error="Database not available!")
