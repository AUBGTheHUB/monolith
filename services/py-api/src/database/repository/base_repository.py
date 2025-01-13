from abc import abstractmethod, ABC
from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from result import Result, Err

from src.database.model.base_model import BaseDbModel


# Across the project we use the result pattern for better error handling
# https://www.milanjovanovic.tech/blog/functional-error-handling-in-dotnet-with-the-result-pattern
# https://github.com/rustedpy/result


# Py3.12 Generics: https://www.youtube.com/watch?v=TkDg3EHwC1g
class CRUDRepository[T: BaseDbModel](ABC):
    """A Generic Interface for CRUD operations over a particular collection in Mongo. Implementations should pass
    the concrete type like this::

        class ParticipantsRepository(CRUDRepository[Participant]):
            async def create(self, participant: Participant) -> Result[Participant, Exception]:
                pass

    """

    @abstractmethod
    async def create(self, obj: T, session: Optional[AsyncIOMotorClientSession] = None) -> Result[T, Exception]:
        """Create a new document in a particular collection in Mongo.

        Args:
            obj: The data to be inserted, it should be represented as a db Model.
            session: If provided, this operation will be executed within a session context, where other related
                operations might also be running as part of a sequence. It is also used to execute the operation in a
                transaction. For more info check the `TransactionManager` class
        """
        raise NotImplementedError()

    @abstractmethod
    async def fetch_by_id(self, obj_id: str) -> Result[T, Err]:
        # TODO The implementer should catch invalid ObjectID format
        raise NotImplementedError()

    @abstractmethod
    async def fetch_all(self) -> Result[List[T], Exception]:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self,
        obj_id: str,
        obj: BaseModel,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[T, Exception]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result[T, Exception]:
        raise NotImplementedError()
