from unittest.mock import Mock, MagicMock, AsyncMock

import pytest
from result import Err

from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import PongResponse, ErrResponse


@pytest.mark.asyncio
async def test_ping_handler(db_manager_mock: Mock, response_mock: MagicMock) -> None:
    # Mock that async_ping_db return no error
    db_manager_mock.async_ping_db = AsyncMock(return_value=None)
    handler = UtilityHandlers(db_manager_mock)

    result = await handler.ping_services(response=response_mock)

    assert isinstance(result, PongResponse)
    assert result == PongResponse(message="pong")


@pytest.mark.asyncio
async def test_ping_handler_error(db_manager_mock: Mock, response_mock: MagicMock) -> None:
    # Mock that async_ping_db return no error
    db_manager_mock.async_ping_db = AsyncMock(return_value=Err("Test error"))
    handler = UtilityHandlers(db_manager_mock)

    result = await handler.ping_services(response=response_mock)

    assert isinstance(result, ErrResponse)
    assert result == ErrResponse(error="Database not available!")
