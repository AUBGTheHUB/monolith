import pytest
from unittest.mock import patch, MagicMock
from result import Err
from src.database.db_manager import DatabaseManager


@pytest.mark.asyncio
async def test_close_all_connections_when_client_initialized() -> None:
    # Instantiate the DatabaseManager
    db_manager = DatabaseManager()

    # Mock the _client attribute using MagicMock
    with patch.object(db_manager, "_client", new_callable=MagicMock) as mock_client:
        db_manager.close_all_connections()
        # Ensure the close method is called
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_close_all_connections_when_client_not_initialized() -> None:

    db_manager = DatabaseManager()

    db_manager._client = None
    result = db_manager.close_all_connections()
    assert isinstance(result, Err)
    assert result.err_value == "The database client is not initialized!"
