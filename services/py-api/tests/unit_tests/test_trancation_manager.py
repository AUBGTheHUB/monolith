from unittest.mock import AsyncMock, patch, MagicMock, Mock

import pytest
from pymongo.errors import PyMongoError
from result import Ok, Err

from src.database.db_manager import DatabaseManager
from src.database.transaction_manager import TransactionManager


@pytest.fixture
def setup_transaction_manager(db_manager_mock: DatabaseManager) -> TransactionManager:
    return TransactionManager(db_manager_mock)


# Define a custom exception to simulate transient transaction error
class TransientTransactionError(PyMongoError):
    def has_error_label(self, label: str) -> bool:
        return label == "TransientTransactionError"


@pytest.mark.asyncio
async def test_retry_tx_success() -> None:
    # Define a db operation that succeeds immediately
    mock_db_operation = AsyncMock(return_value=Ok("Success"))

    result = await TransactionManager._retry_tx(mock_db_operation)

    mock_db_operation.assert_awaited_once()
    assert result == Ok("Success")


@pytest.mark.asyncio
async def test_retry_tx_transient_error_with_retry() -> None:
    # Simulate transient error on the first call, then success
    mock_db_operation = AsyncMock(side_effect=[TransientTransactionError(), Ok("Success")])

    # Patch sleep for faster testing
    with patch("src.database.transaction_manager.sleep", AsyncMock()):
        result = await TransactionManager._retry_tx(mock_db_operation)

    # Called twice due to retry
    assert mock_db_operation.call_count == 2
    assert result == Ok("Success")


@pytest.mark.asyncio
async def test_retry_tx_non_retryable_error() -> None:
    # Simulate a non-retryable error
    mock_db_operation = AsyncMock(side_effect=PyMongoError("Non-retryable error"))

    with pytest.raises(PyMongoError) as exc:
        await TransactionManager._retry_tx(mock_db_operation)

    # Should only be called once, no retry
    mock_db_operation.assert_awaited_once()
    assert str(exc.value) == "Non-retryable error"


@pytest.mark.asyncio
async def test_retry_tx_exhaust_retries() -> None:
    # Simulate a transient error that keeps failing
    mock_db_operation = AsyncMock(side_effect=TransientTransactionError())

    # Patch sleep for faster tests
    with patch("src.database.transaction_manager.sleep", AsyncMock()):
        with pytest.raises(PyMongoError) as exc:
            await TransactionManager._retry_tx(mock_db_operation)

    # Should be called max_retries times
    assert mock_db_operation.call_count == 3
    assert str(exc.value) == "Transaction failed after maximum retries"


@pytest.mark.asyncio
async def test_with_transaction_success(setup_transaction_manager: TransactionManager, db_manager_mock: Mock) -> None:
    tx_manager = setup_transaction_manager

    # Create a mock session to be returned by the start_session method
    mock_session = MagicMock()
    db_manager_mock.client.start_session.return_value = mock_session

    # `start_transaction` is synchronous and returns a context manager _MotorTransactionContext, that's why we need
    # MagicMock
    mock_session.start_transaction = MagicMock()
    mock_session.commit_transaction = AsyncMock()  # `commit_transaction` is async
    mock_session.abort_transaction = AsyncMock()  # `abort_transaction` is async
    mock_session.end_session = AsyncMock()  # `end_session` is async

    # Mock callback function that represents the transaction
    async def mock_callback(session: MagicMock) -> Ok:
        return Ok("Success")

    result = await tx_manager.with_transaction(mock_callback)

    db_manager_mock.client.start_session.assert_called_once()
    mock_session.start_transaction.assert_called_once()
    mock_session.commit_transaction.assert_awaited_once()
    mock_session.abort_transaction.assert_not_called()
    mock_session.end_session.assert_awaited_once()
    assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_failure(setup_transaction_manager: TransactionManager, db_manager_mock: Mock) -> None:
    tx_manager = setup_transaction_manager

    # Create a mock session to be returned by the start_session method
    mock_session = MagicMock()
    db_manager_mock.client.start_session.return_value = mock_session

    # `start_transaction` is synchronous and returns a context manager _MotorTransactionContext, that's why we need
    # MagicMock
    mock_session.start_transaction = MagicMock()
    mock_session.commit_transaction = AsyncMock()  # `commit_transaction` is async
    mock_session.abort_transaction = AsyncMock()  # `abort_transaction` is async
    mock_session.end_session = AsyncMock()  # `end_session` is async

    # Define a callback function that raises an exception
    async def mock_callback(session: AsyncMock) -> Err:
        return Err(ValueError("Simulated failure"))

    result = await tx_manager.with_transaction(mock_callback)

    db_manager_mock.client.start_session.assert_called_once()
    mock_session.start_transaction.assert_called_once()
    mock_session.abort_transaction.assert_awaited_once()
    mock_session.commit_transaction.assert_not_called()
    mock_session.end_session.assert_awaited_once()
    assert isinstance(result, Err)
