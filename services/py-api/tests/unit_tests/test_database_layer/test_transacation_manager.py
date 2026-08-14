from unittest.mock import AsyncMock, patch

import pytest
from pymongo.errors import PyMongoError
from result import Ok, Err
from src.database.mongo.transaction_manager import MongoTransactionManager
from tests.unit_tests.conftest import MongoDbClientMock, MongoDbManagerMock, MongoDbClientSessionMock


@pytest.fixture
def tx_manager(mongo_db_client_mock: MongoDbClientMock) -> MongoTransactionManager:
    return MongoTransactionManager(mongo_db_client_mock)


# Define a custom exception to simulate transient transaction error
class TransientTransactionError(PyMongoError):
    def has_error_label(self, label: str) -> bool:
        return label == "TransientTransactionError"


# Define a custom exception to simulate unknown transaction commit result error
class UnknownTransactionCommitResult(PyMongoError):
    def has_error_label(self, label: str) -> bool:
        return label == "UnknownTransactionCommitResult"


@pytest.mark.asyncio
async def test_with_transaction_success(
    tx_manager: MongoTransactionManager,
    mongo_db_manager_mock: MongoDbManagerMock,
    mongo_db_session_mock: MongoDbClientSessionMock,
) -> None:

    # Given
    # Mock a successful db operation
    mock_db_operation = AsyncMock(return_value=Ok("Success"))

    # When
    result = await tx_manager.with_transaction(mock_db_operation)

    # Then
    mongo_db_session_mock.start_transaction.assert_awaited_once()
    mongo_db_session_mock.commit_transaction.assert_awaited_once()
    mongo_db_session_mock.abort_transaction.assert_not_called()
    mongo_db_session_mock.end_session.assert_awaited_once()
    assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_transient_error(
    tx_manager: MongoTransactionManager,
    mongo_db_manager_mock: MongoDbManagerMock,
    mongo_db_session_mock: MongoDbClientSessionMock,
) -> None:

    # Given
    # Simulate transient error on the first call, then success
    mock_db_operation = AsyncMock(side_effect=[Err(TransientTransactionError()), Ok("Success")])

    # We patch the sleep function for faster testing
    with patch("src.database.mongo.transaction_manager.sleep", new=AsyncMock()):
        # When
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then
        mongo_db_session_mock.start_transaction.assert_awaited_once()
        mongo_db_session_mock.commit_transaction.assert_awaited_once()
        mongo_db_session_mock.abort_transaction.assert_not_called()
        mongo_db_session_mock.end_session.assert_awaited_once()

        # On the first call it failed and on the second call it succeeded
        assert mock_db_operation.call_count == 2
        assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_unknown_commit_result_error(
    tx_manager: MongoTransactionManager,
    mongo_db_manager_mock: MongoDbManagerMock,
    mongo_db_session_mock: MongoDbClientSessionMock,
) -> None:

    # Given
    # Mock a successful db operation
    mock_db_operation = AsyncMock(return_value=Ok("Success"))
    # Mock a commit failing first and then succeeding
    mongo_db_session_mock.commit_transaction = AsyncMock(side_effect=[UnknownTransactionCommitResult("Test err"), None])

    # We patch the sleep function for faster testing
    with patch("src.database.mongo.transaction_manager.sleep", new=AsyncMock()):
        # When
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then
        mongo_db_session_mock.start_transaction.assert_awaited_once()
        mongo_db_session_mock.abort_transaction.assert_not_called()
        mongo_db_session_mock.end_session.assert_awaited_once()

        # On the first call it failed and on the second call it succeeded
        assert mongo_db_session_mock.commit_transaction.call_count == 2
        assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_exhaust_retries(
    tx_manager: MongoTransactionManager,
    mongo_db_manager_mock: MongoDbManagerMock,
    mongo_db_session_mock: MongoDbClientSessionMock,
) -> None:

    # Given
    # Simulate a transient error that keeps failing
    mock_db_operation = AsyncMock(return_value=Err(TransientTransactionError()))

    # We patch the sleep function for faster testing
    with patch("src.database.mongo.transaction_manager.sleep", new=AsyncMock()):
        # When
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then
        mongo_db_session_mock.start_transaction.assert_awaited_once()
        mongo_db_session_mock.commit_transaction.assert_not_called()
        mongo_db_session_mock.abort_transaction.assert_awaited_once()
        mongo_db_session_mock.end_session.assert_awaited_once()

        # Should be called max_retries times
        assert mock_db_operation.call_count == 3
        assert isinstance(result, Err)
        assert isinstance(result.err_value, PyMongoError)


@pytest.mark.asyncio
async def test_with_transaction_unknown_commit_result_exhaust_retries(
    tx_manager: MongoTransactionManager,
    mongo_db_manager_mock: MongoDbManagerMock,
    mongo_db_session_mock: MongoDbClientSessionMock,
) -> None:

    # Given
    # Mock a successful db operation
    mock_db_operation = AsyncMock(return_value=Ok("Success"))
    # Simulate a commit error that keeps failing
    mongo_db_session_mock.commit_transaction = AsyncMock(side_effect=UnknownTransactionCommitResult("Test err"))

    # We patch the sleep function for faster testing
    with patch("src.database.mongo.transaction_manager.sleep", new=AsyncMock()):
        # When
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then
        mongo_db_session_mock.start_transaction.assert_awaited_once()
        mongo_db_session_mock.abort_transaction.assert_awaited_once()
        mongo_db_session_mock.end_session.assert_awaited_once()

        # Should be called max_retries times
        assert mongo_db_session_mock.commit_transaction.call_count == 3
        assert isinstance(result, Err)
        assert isinstance(result.err_value, PyMongoError)
