from result import Err, Result

from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.server.schemas.request_schemas.admin.past_event_schemas import PastEventPostReqData, PastEventPutReqData


class PastEventsService:
    def __init__(self, repo: PastEventsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[PastEvent], Exception]:
        return await self._repo.fetch_all()

    async def get(self, event_id: str) -> Result[PastEvent, Exception]:
        return await self._repo.fetch_by_id(event_id)

    async def create(self, data: PastEventPostReqData) -> Result[PastEvent, Exception]:
        try:
            past_event = PastEvent(
                title=str(data.title),
                cover_picture=str(data.cover_picture),
                tags=[str(tag) for tag in data.tags],
            )
            return await self._repo.create(past_event)
        except Exception as exc:
            return Err(exc)

    async def update(self, event_id: str, data: PastEventPutReqData) -> Result[PastEvent, Exception]:
        try:
            update_params = UpdatePastEventParams(
                title=str(data.title),
                cover_picture=str(data.cover_picture),
                tags=[str(tag) for tag in data.tags],
            )
            return await self._repo.update(event_id, update_params)
        except Exception as exc:
            return Err(exc)

    async def delete(self, event_id: str) -> Result[PastEvent, Exception]:
        return await self._repo.delete(event_id)
