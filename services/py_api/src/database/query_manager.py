from collections.abc import Callable
from time import monotonic
from typing import Any, Awaitable, TypeVar

from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.db_manager import DatabaseManager
from src.utils import SingletonMeta

LOG = get_logger()

T = TypeVar("T")


class QueryManager(metaclass=SingletonMeta):
    _RETRY_TRANSACTION_DEADLINE_SEC = 3

    def __init__(self, db_manager: DatabaseManager, collection: str) -> None:
        self._client = db_manager.client
        self._collection = self._client[db_manager.DB_NAME][collection]

    def _deadline_exceeded(self, start_time: float) -> bool:
        return monotonic() - start_time < self._RETRY_TRANSACTION_DEADLINE_SEC

    async def _retry_tx(
        self, func: Callable[..., Awaitable[T]], session: AsyncIOMotorClientSession, *args: Any, **kwargs: Any
    ) -> T:
        """
        If there was a TransientTransactionError, retries the transaction up to max_retries or
        until the deadline is exceeded, whichever is first.
        Inspired by AgnosticClientSession.with_transaction()
        https://stackoverflow.com/questions/52153538/what-is-a-transienttransactionerror-in-mongoose-or-mongodb
        """
        max_retries = 3
        start_time = monotonic()

        for retry in range(max_retries):
            try:
                return await func(*args, session=session, **kwargs)
            except PyMongoError as exc:
                if exc.has_error_label("TransientTransactionError") and not self._deadline_exceeded(start_time):
                    LOG.debug("Retrying transaction retry{}".format(retry))
                    continue
                # If it's a non-retryable error, or we've exceeded the deadline, re-raise
                raise exc

        raise RuntimeError("Transaction failed after maximum retries")

    async def create_obj_tx(self, input_data: BaseModel) -> Result[InsertOneResult, str]:
        # TODO: add check if unique constraint fails
        """Creates an obj in Mongo via a transaction"""
        # https://www.mongodb.com/docs/manual/core/transactions/
        session = await self._client.start_session()
        try:
            session.start_transaction()
            LOG.debug("Inserting obj in Mongo via transaction")

            inserted_result = await self._retry_tx(self._collection.insert_one, session, input_data.model_dump())
            await session.commit_transaction()

            return Ok(inserted_result)

        except Exception as e:
            LOG.debug("Aborting transaction due to err {}".format(e))
            await session.abort_transaction()
            return Err(e.args[0])

        finally:
            LOG.debug("Closing DB session")
            # Finish this session. If a transaction has started, abort it.
            await session.end_session()

    async def fetch_by_id(self) -> Result:
        pass

    async def fetch_all(self) -> Result:
        # TODO: Finish. Use the self._collection if needed
        pass

    async def update_obj_tx(self) -> Result:
        # TODO: Finish
        pass

    async def delete_obj_tx(self) -> Result:
        # TODO: Finish
        pass
