# mypy: disable-error-code=no-any-return
# This is because we have Generic methods
from asyncio import sleep
from typing import Callable, Any, Awaitable

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorClient
from pymongo.errors import PyMongoError
from result import Err, is_err, Result, is_ok
from structlog.stdlib import get_logger

LOG = get_logger()


class MongoTransactionManager:
    """This class is responsible for executing multiple mongo db queries such as insert_one or update_on in a
    transactional context. It manages operations such as starting, commiting, aborting and retrying a transaction.
    The terms you will see in the code below:

    `session` - a Mongo ClientSession provides the context in which to execute multiple operations in a specific
    sequence, isolating them from operations in other sessions and transactions to prevent conflicts and maintain data
    consistency. In other words the session provides Causal Consistency to the operations in the transaction.
    https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/#causal-consistency

    `transaction` - Ensures atomicity within this session context, meaning that all operations in the sequence succeed
    together or fail together. If any operation fails, the entire sequence is rolled back, so changes to the database
    are not made

    To learn more about Mongo ClientSession visit:
    https://pymongo.readthedocs.io/en/stable/api/pymongo/client_session.html#pymongo.client_session.ClientSession

    To learn more about Transactions in Mongo visit: https://www.mongodb.com/docs/manual/core/transactions/

    To learn more about Isolation Levels visit:
    https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/
    """

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self._client = client

    @staticmethod
    async def _retry_tx(func: Callable[..., Awaitable[Result]], *args: Any, **kwargs: Any) -> Result:
        """
        If there was a TransientTransactionError during execution, retries the transaction with exponential backoff up
        to max_retries times. Having an exponential backoff increases our chances of success if there was a temporary
        network issue.

        Inspired by:
        https://www.mongodb.com/docs/manual/core/transactions-in-applications/#example-1
        https://motor.readthedocs.io/en/stable/api-tornado/motor_client_session.html#motor.motor_tornado.MotorClientSession.with_transaction
        https://stackoverflow.com/questions/52153538/what-is-a-transienttransactionerror-in-mongoose-or-mongodb

        Args:
            func: The func is the callback that is passed to the with_transaction() method. It should return a
             Result[Ok, Err]
        """
        max_retries = 3
        delay = 0.1  # initial delay in seconds

        # range is exclusive that's why we do max_retries + 1
        for retry in range(1, max_retries + 1):

            # Call the callback.
            result = await func(*args, **kwargs)

            if is_ok(result):
                return result

            # Check if it is a retryable error - a TransientTransactionError
            if isinstance(result.err_value, PyMongoError) and result.err_value.has_error_label(
                "TransientTransactionError"
            ):

                # Retry the transaction by taking the control to the start of the loop using `continue`
                LOG.debug("Retrying transaction...", retry=retry, callback=func)
                await sleep(delay)
                delay *= 2  # Apply Exponential Backoff
                continue

            # If the exception it's a non-retryable error return it in order to be caught on an upper level
            LOG.error("Un-retryable error during transaction!", err=result.err_value, callback=func)
            return result

        return Err(PyMongoError("Transaction failed after maximum retries"))

    @staticmethod
    async def _retry_commit(session: AsyncIOMotorClientSession) -> None:
        """
        Uses the same logic for the retries as the _retry_tx (exponential backoff)
        Inspired by:
        https://www.mongodb.com/docs/manual/core/transactions-in-applications/#example-1

        Raises:
            PyMongoError
        """
        max_retries = 3
        delay = 0.1  # initial delay in seconds

        # range is exclusive that's why we do max_retries + 1
        for retry in range(1, max_retries + 1):
            try:
                # The commit_transaction method does not return anything, and we use the return to exit the loop
                # if no Exception is encountered
                return await session.commit_transaction()
            except PyMongoError as exc:
                if exc.has_error_label("UnknownTransactionCommitResult"):
                    LOG.debug("Retrying to commit transaction...", retry=retry)
                    await sleep(delay)
                    delay *= 2  # exponential backoff
                    continue

                # If the exception it's a non-retryable error re-raise it in order to be caught on an upper level
                LOG.error("Commiting the transaction failed", err=exc)
                raise exc

        raise PyMongoError("Commiting transaction failed after maximum retries")

    async def with_transaction[T](self, callback: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """
        A generic method used for executing a callback in a transaction. This method is generic as we want the
        with_transaction method to have the return type of the passed callback function. The method is responsible for
        starting a transaction and commiting it. In case of an Exception the transaction is automatically aborted.

        Note: The default with_transaction method from the `motor` library will stop retrying the transaction after 120 seconds
        have elapsed. However, since we want a shorter duration until the transaction is aborted, we have implemented a _retry_tx
        method and _retry_commit method that will abort the transaction when the maximum number of retries is reached in any of
        the retry methods.

        The ``callback`` could be a function grouping multiple operations. For example::

        async def callback(session):
            await participants.insert_one({"test":"test"} session=session)
            await teams.update_one({"test":"test"} session=session)

        await tx_manager.with_transaction(callback)

        To learn more about Generics visit:
        https://docs.python.org/3/library/typing.html#generics
        https://www.youtube.com/watch?v=q6ujWWaRdbA
        """

        session = await self._client.start_session()
        try:
            session.start_transaction()
            LOG.debug("Starting transaction")

            result = await self._retry_tx(callback, *args, session=session, **kwargs)
            if is_err(result):
                LOG.warning("Aborting transaction due to err", err=result.err_value)
                await session.abort_transaction()
                return result

            await self._retry_commit(session)
            LOG.debug("Transaction commited")

            return result

        except Exception as e:
            LOG.exception("Aborting transaction due to error", error=e)
            await session.abort_transaction()
            return Err(e)

        finally:
            LOG.debug("Closing DB session")
            # Finish this session. If a transaction has started, abort it.
            await session.end_session()


def mongo_tx_manager_provider(client: AsyncIOMotorClient) -> MongoTransactionManager:
    """
    Args:
        client: A singleton AsyncIOMotorClient instance

    Returns:
        A TransactionManager instance
    """
    return MongoTransactionManager(client=client)
