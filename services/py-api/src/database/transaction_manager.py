# mypy: disable-error-code=no-any-return
# This is because we have Generic methods

from time import monotonic
from typing import Callable, Any, TypeVar, Awaitable

from pymongo.errors import PyMongoError
from result import Err, is_err, Result
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager

LOG = get_logger()

T = TypeVar("T")
E = TypeVar("E")


class TransactionManager:
    _RETRY_TRANSACTION_DEADLINE_SEC = 3

    def __init__(self, db_manager: DatabaseManager) -> None:
        self._client = db_manager.client

    def _deadline_exceeded(self, start_time: float) -> bool:
        return monotonic() - start_time > self._RETRY_TRANSACTION_DEADLINE_SEC

    async def _retry_tx(self, func: Callable[..., Awaitable[Result[T, E]]], *args: Any, **kwargs: Any) -> Result[T, E]:
        """
        If there was a TransientTransactionError, retries the transaction up to max_retries or
        until the deadline is exceeded, whichever is first.
        Inspired by AgnosticClientSession.with_transaction()
        https://motor.readthedocs.io/en/stable/api-tornado/motor_client_session.html#motor.motor_tornado.MotorClientSession.with_transaction
        https://stackoverflow.com/questions/52153538/what-is-a-transienttransactionerror-in-mongoose-or-mongodb
        """
        max_retries = 3
        start_time = monotonic()

        for retry in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except PyMongoError as exc:
                if exc.has_error_label("TransientTransactionError") and not self._deadline_exceeded(start_time):
                    LOG.debug("Retrying transaction retry {}".format(retry))
                    continue
                # If it's a non-retryable error, or we've exceeded the deadline, re-raise
                raise exc

        raise RuntimeError("Transaction failed after maximum retries")

    async def with_transaction(self, callback: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """
        A generic method used for executing a callback in a transaction. The method starts the transaction and commits
        it. In case of an Exception the transaction is automatically aborted.

        The ``callback`` could be a function grouping multiple operations. For example::

        async def callback(session):
            await participants.insert_one({"test":"test"} session=session)
            await teams.update_one({"test":"test"} session=session)

        await tx_manager.with_transaction(callback)
        """

        session = await self._client.start_session()
        try:
            session.start_transaction()
            LOG.debug("Starting transaction")

            result = await self._retry_tx(callback, *args, session=session, **kwargs)
            if is_err(result):
                LOG.exception("Aborting transaction due to err {}".format(result.value))
                await session.abort_transaction()
                return result

            await session.commit_transaction()
            LOG.debug("Transaction commited")

            return result
        except Exception as e:
            LOG.exception("Aborting transaction due to err {}".format(e))
            await session.abort_transaction()
            return Err(e)
        finally:
            LOG.debug("Closing DB session")
            # Finish this session. If a transaction has started, abort it.
            await session.end_session()
