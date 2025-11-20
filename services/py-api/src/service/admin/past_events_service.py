from result import Result, Err

from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.repository.admin.past_events_repository import PastEventsRepository


class PastEventsService:
    def __init__(self, repo: PastEventsRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[PastEvent], Exception]:
        return Err(NotImplementedError())

    async def get(self, event_id: str) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def create(self, event: PastEvent) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def update(self, event_id: str, params: UpdatePastEventParams) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())

    async def delete(self, event_id: str) -> Result[PastEvent, Exception]:
        return Err(NotImplementedError())
