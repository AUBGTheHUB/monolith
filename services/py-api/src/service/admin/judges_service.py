from typing import Optional

from fastapi import UploadFile
from pydantic import HttpUrl
from result import Result

from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.repository.admin.judges_repository import JudgesRepository
from src.exception import JudgeNotFoundError
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class JudgesService:
    def __init__(self, repo: JudgesRepository, image_storing_service: ImageStoringService) -> None:
        self._repo = repo
        self._image_storing_service = image_storing_service

    async def get_all(self) -> Result[list[Judge], Exception]:
        return await self._repo.fetch_all()

    async def get(self, judge_id: str) -> Result[Judge, JudgeNotFoundError | Exception]:
        return await self._repo.fetch_by_id(judge_id)

    async def create(
        self, name: str, company: str, job_title: str, avatar: UploadFile, linkedin_url: Optional[HttpUrl] = None
    ) -> Result[Judge, Exception]:
        judge = Judge(name=name, company=company, job_title=job_title, avatar_url="", linkedin_url=str(linkedin_url))
        avatar_url = await self._image_storing_service.upload_image(file=avatar, file_name=f"judges/{str(judge.id)}")
        judge.avatar_url = str(avatar_url)

        return await self._repo.create(judge)

    async def update(
        self,
        judge_id: str,
        name: str | None = None,
        company: str | None = None,
        job_title: str | None = None,
        avatar: UploadFile | None = None,
        linkedin_url: Optional[HttpUrl] = None,
    ) -> Result[Judge, Exception]:
        params = UpdateJudgeParams(name=name, company=company, job_title=job_title, linkedin_url=linkedin_url)

        if avatar is not None:
            await self._image_storing_service.upload_image(file=avatar, file_name=f"judges/{str(judge_id)}")

        return await self._repo.update(judge_id, params)

    async def delete(self, judge_id: str) -> Result[Judge, Exception]:
        result = await self._repo.delete(judge_id)

        if result.is_ok():
            self._image_storing_service.delete_image(f"judges/{str(judge_id)}")

        return result
