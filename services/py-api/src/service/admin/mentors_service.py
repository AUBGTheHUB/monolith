from typing import Optional

from fastapi import UploadFile
from pydantic import HttpUrl
from result import Result

from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class MentorsService:
    def __init__(self, repo: MentorsRepository, image_storing_service: ImageStoringService) -> None:
        self._repo = repo
        self._image_storing_service = image_storing_service

    async def get_all(self) -> Result[list[Mentor], Exception]:
        return await self._repo.fetch_all()

    async def get(self, mentor_id: str) -> Result[Mentor, Exception]:
        return await self._repo.fetch_by_id(mentor_id)

    async def create(
        self,
        name: str,
        company: str,
        job_title: str,
        avatar: UploadFile,
        linkedin_url: Optional[HttpUrl] = None,
    ) -> Result[Mentor, Exception]:
        mentor = Mentor(name=name, company=company, job_title=job_title, avatar_url="", linkedin_url=str(linkedin_url))
        avatar_url = await self._image_storing_service.upload_image(file=avatar, file_name=f"mentors/{str(mentor.id)}")
        mentor.avatar_url = str(avatar_url)

        return await self._repo.create(mentor)

    async def update(
        self,
        mentor_id: str,
        name: str | None = None,
        company: str | None = None,
        job_title: str | None = None,
        avatar: UploadFile | None = None,
        linkedin_url: Optional[HttpUrl] = None,
    ) -> Result[Mentor, Exception]:

        if avatar is not None:
            await self._image_storing_service.upload_image(file=avatar, file_name=f"mentors/{str(mentor_id)}")

        params = UpdateMentorParams(name=name, company=company, job_title=job_title, linkedin_url=str(linkedin_url))
        return await self._repo.update(mentor_id, params)

    async def delete(self, mentor_id: str) -> Result[Mentor, Exception]:
        result = await self._repo.delete(mentor_id)

        if result.is_ok():
            self._image_storing_service.delete_image(f"mentors/{str(mentor_id)}")

        return result
