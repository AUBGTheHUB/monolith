from abc import abstractmethod, ABC
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel
from result import Result


# Across the project we use the result pattern for better error handling
# https://www.milanjovanovic.tech/blog/functional-error-handling-in-dotnet-with-the-result-pattern
# https://github.com/rustedpy/result


class CRUDRepository(ABC):
    """An Interface for CRUD operations over a particular collection in Mongo"""

    @abstractmethod
    async def create(self, input_data: BaseModel, session: Optional[AsyncIOMotorClientSession] = None) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def fetch_by_id(self, obj_id: str) -> Result:
        # TODO The implementer should catch invalid ObjectID format
        raise NotImplementedError()

    @abstractmethod
    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, obj_id: str, input_data: BaseModel, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result:
        raise NotImplementedError()
