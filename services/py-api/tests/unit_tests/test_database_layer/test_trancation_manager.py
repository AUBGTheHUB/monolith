from typing import cast
from unittest.mock import AsyncMock, patch
from motor.motor_asyncio import AsyncIOMotorClient

import pytest
from pymongo.errors import PyMongoError
from result import Ok, Err

from src.database.transaction_managers import MongoTransactionManager
from tests.unit_tests.conftest import MotorDbClientMock, MotorDbClientSessionMock


@pytest.fixture
def tx_manager(motor_db_client_mock: MotorDbClientMock) -> MongoTransactionManager:
    return MongoTransactionManager(cast(AsyncIOMotorClient, motor_db_client_mock))


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
    motor_db_client_mock: MotorDbClientMock,
    motor_db_session_mock: MotorDbClientSessionMock,
    tx_manager: MongoTransactionManager,
) -> None:
    # Given a successful db operation callback (the db_operation callback returns a Result)
    mock_db_operation = AsyncMock(return_value=Ok("Success"))

    # When we execute the with_transaction method
    result = await tx_manager.with_transaction(mock_db_operation)

    # Then the session would have started and the transaction would be successfully completed
    motor_db_client_mock.start_session.assert_called_once()

    motor_db_session_mock.start_transaction.assert_called_once()
    motor_db_session_mock.commit_transaction.assert_awaited_once()
    motor_db_session_mock.abort_transaction.assert_not_called()
    motor_db_session_mock.end_session.assert_awaited_once()

    assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_transient_error(
    motor_db_session_mock: MotorDbClientSessionMock,
    motor_db_client_mock: MotorDbClientMock,
    tx_manager: MongoTransactionManager,
) -> None:
    # Given a transient error on the first call and a success on the second one
    # (the db_operation callback returns a Result)
    mock_db_operation = AsyncMock(side_effect=[Err(TransientTransactionError()), Ok("Success")])

    # We patch the sleep function for faster testing
    with patch("src.database.transaction_managers.sleep", new=AsyncMock()):
        # When we execute the with_transaction method
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then the transaction should have failed on the first try
        motor_db_client_mock.start_session.assert_called_once()
        motor_db_session_mock.start_transaction.assert_called_once()
        motor_db_session_mock.commit_transaction.assert_awaited_once()
        motor_db_session_mock.abort_transaction.assert_not_called()
        motor_db_session_mock.end_session.assert_awaited_once()

        # And succeeded on the second
        assert mock_db_operation.call_count == 2
        assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_unknown_commit_result_error(
    motor_db_session_mock: MotorDbClientSessionMock,
    motor_db_client_mock: MotorDbClientMock,
    tx_manager: MongoTransactionManager,
) -> None:
    # Given a successful db operation and commit_transaction failing first and then succeeding
    # (the db_operation callback returns a Result)
    mock_db_operation = AsyncMock(return_value=Ok("Success"))
    # And an UnknownTransactionCommitResult from commit_transaction on the first call
    motor_db_session_mock.commit_transaction.side_effect = [UnknownTransactionCommitResult("Test err"), None]

    # We patch the sleep function for faster testing
    with patch("src.database.transaction_managers.sleep", new=AsyncMock()):
        # When we execute the with_transaction method
        result = await tx_manager.with_transaction(mock_db_operation)

        # Then it fails on the first call
        motor_db_client_mock.start_session.assert_called_once()
        motor_db_session_mock.start_transaction.assert_called_once()
        motor_db_session_mock.abort_transaction.assert_not_called()
        motor_db_session_mock.end_session.assert_awaited_once()

        # And succeeds on the second
        assert motor_db_session_mock.commit_transaction.call_count == 2
        assert result == Ok("Success")


@pytest.mark.asyncio
async def test_with_transaction_exhaust_retries(
    motor_db_session_mock: MotorDbClientSessionMock,
    motor_db_client_mock: MotorDbClientMock,
    tx_manager: MongoTransactionManager,
) -> None:
    # Given a transient error that keeps failing
    # (the db_operation callback returns a Result)
    mock_db_operation = AsyncMock(return_value=Err(TransientTransactionError()))

    # We patch the sleep function for faster testing
    with patch("src.database.transaction_managers.sleep", new=AsyncMock()):
        # When we execute the with_transaction method
        result = await tx_manager.with_transaction(mock_db_operation)

        motor_db_client_mock.start_session.assert_called_once()
        motor_db_session_mock.start_transaction.assert_called_once()
        motor_db_session_mock.commit_transaction.assert_not_called()
        motor_db_session_mock.abort_transaction.assert_awaited_once()
        motor_db_session_mock.end_session.assert_awaited_once()

        # Then it should be called max_retries times
        assert mock_db_operation.call_count == 3
        assert isinstance(result, Err)
        assert isinstance(result.err_value, PyMongoError)


@pytest.mark.asyncio
async def test_with_transaction_unknown_commit_result_exhaust_retries(
    motor_db_session_mock: MotorDbClientSessionMock,
    motor_db_client_mock: MotorDbClientMock,
    tx_manager: MongoTransactionManager,
) -> None:
    # Given a successful db operation
    mock_db_operation = AsyncMock(return_value=Ok("Success"))
    # And an UnknownTransactionCommitResult from commit_transaction that keeps occurring
    motor_db_session_mock.commit_transaction.side_effect = UnknownTransactionCommitResult("Test err")

    # We patch the sleep function for faster testing
    with patch("src.database.transaction_managers.sleep", new=AsyncMock()):
        # When we execute the with_transaction method
        result = await tx_manager.with_transaction(mock_db_operation)

        motor_db_client_mock.start_session.assert_called_once()
        motor_db_session_mock.start_transaction.assert_called_once()
        motor_db_session_mock.abort_transaction.assert_awaited_once()
        motor_db_session_mock.end_session.assert_awaited_once()

        # Then it should be called max_retries times
        assert motor_db_session_mock.commit_transaction.call_count == 3
        assert isinstance(result, Err)
        assert isinstance(result.err_value, PyMongoError)
