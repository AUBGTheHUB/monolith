from abc import abstractmethod, ABC

from click.testing import Result
from pydantic import BaseModel


class CRUDRepository(ABC):
    @abstractmethod
    async def create(self, input_data: BaseModel) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def fetch_by_id(self, obj_id: str) -> Result:
        # TODO The implementer should catch invalid ObjectID format
        raise NotImplementedError()

    @abstractmethod
    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def update(self) -> Result:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, obj_id: str) -> Result:
        raise NotImplementedError()
