from result import Result

from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.server.schemas.request_schemas.admin.mentor_schemas import MentorPostReqData, MentorPatchReqData


class MentorsService:
    def __init__(self, repo: MentorsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Mentor], Exception]:
        return await self._repo.fetch_all()

    async def get(self, mentor_id: str) -> Result[Mentor, Exception]:
        return await self._repo.fetch_by_id(mentor_id)

    async def create(self, data: MentorPostReqData) -> Result[Mentor, Exception]:
        mentor = Mentor(**data.model_dump())
        return await self._repo.create(mentor)

    async def update(self, mentor_id: str, data: MentorPatchReqData) -> Result[Mentor, Exception]:
        params = UpdateMentorParams(**data.model_dump())
        return await self._repo.update(mentor_id, params)

    async def delete(self, mentor_id: str) -> Result[Mentor, Exception]:
        return await self._repo.delete(mentor_id)
