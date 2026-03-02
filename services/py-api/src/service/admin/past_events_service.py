from typing import Optional

from fastapi import UploadFile
from result import Result

from src.database.model.admin.past_event_model import PastEvent, UpdatePastEventParams
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.exception import PastEventNotFoundError
from src.server.schemas.request_schemas.schemas import NonEmptyStr
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class PastEventsService:
    def __init__(self, repo: PastEventsRepository, image_storing_service: ImageStoringService) -> None:
        self._repo = repo
        self._image_storing_service = image_storing_service

    async def get_all(self) -> Result[list[PastEvent], Exception]:
        return await self._repo.fetch_all()

    async def get(self, event_id: str) -> Result[PastEvent, PastEventNotFoundError | Exception]:
        return await self._repo.fetch_by_id(event_id)

    async def create(
        self, title: NonEmptyStr, cover_picture: UploadFile, tags: list[NonEmptyStr] = []
    ) -> Result[PastEvent, Exception]:
        past_event = PastEvent(
            title=title,
            cover_picture="",
            tags=tags,
        )

        cover_picture_url = await self._image_storing_service.upload_image(
            cover_picture, file_name=f"past_events/{str(past_event.id)}"
        )
        past_event.cover_picture = str(cover_picture_url)

        return await self._repo.create(past_event)

    async def update(
        self,
        event_id: str,
        title: Optional[NonEmptyStr] = None,
        cover_picture: Optional[UploadFile] = None,
        tags: Optional[list[NonEmptyStr]] = None,
    ) -> Result[PastEvent, PastEventNotFoundError | Exception]:

        if cover_picture is not None:
            await self._image_storing_service.upload_image(cover_picture, file_name=f"past_events/{str(event_id)}")

        update_params = UpdatePastEventParams(
            title=title,
            tags=tags,
        )
        return await self._repo.update(event_id, update_params)

    async def delete(self, event_id: str) -> Result[PastEvent, PastEventNotFoundError | Exception]:
        result = await self._repo.delete(event_id)

        if result.is_ok():
            self._image_storing_service.delete_image(f"past_events/{str(event_id)}")

        return result
