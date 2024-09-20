from datetime import datetime

from result import is_err, Result, Ok

from src.database.query_manager import QueryManager
from src.database.repositories.base_repository import CRUDRepository
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody
from src.server.schemas.response_schemas.schemas import ParticipantResponse


class ParticipantsRepository(CRUDRepository):
    # TODO: Implement the rest of the methods
    def __init__(self, query_manager: QueryManager):
        self._query_manager = query_manager

    async def fetch_by_id(self, obj_id: str) -> Result:
        raise NotImplementedError()

    async def fetch_all(self) -> Result:
        raise NotImplementedError()

    async def update(self) -> Result:
        raise NotImplementedError()

    async def delete(self, obj_id: str) -> Result:
        raise NotImplementedError()

    async def create(self, input_data: ParticipantRequestBody) -> Result[ParticipantResponse, str]:
        # TODO: Add unique constraint over email, catch errors accordingly
        result = await self._query_manager.create_obj_tx(input_data)
        if is_err(result):
            return result

        return Ok(
            ParticipantResponse(
                id=str(result.value.inserted_id),
                name=input_data.name,
                email=input_data.email,
                is_admin=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
