from result import Result, Err

from src.database.model.admin.past_event_model import PastEvent
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.server.schemas.admin.request_schemas.schemas import PastEventPostReqData
from src.server.schemas.admin.request_schemas.schemas import PastEventPatchReqData


class PastEventsService:
    def __init__(self, repo: PastEventsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[PastEvent], Exception]:
        return Err(NotImplementedError())

    async def get(self, event_id: str) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def create(self, data: PastEventPostReqData) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def update(self, event_id: str, data: PastEventPatchReqData) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def delete(self, event_id: str) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())
