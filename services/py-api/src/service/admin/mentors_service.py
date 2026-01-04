from result import Result, Err

from src.database.model.admin.mentor_model import Mentor
from src.database.repository.admin.mentors_repository import MentorsRepository
from src.server.schemas.request_schemas.admin.mentor_schemas import MentorPostReqData, MentorPatchReqData


class MentorsService:
    def __init__(self, repo: MentorsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Mentor], Exception]:
        return Err(NotImplementedError())

    async def get(self, mentor_id: str) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def create(self, data: MentorPostReqData) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def update(self, mentor_id: str, data: MentorPatchReqData) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def delete(self, mentor_id: str) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())
