from result import Result, Err

from src.database.model.admin.mentor_model import Mentor, UpdateMentorParams
from src.database.repository.admin.mentors_repository import MentorsRepository


class MentorsService:
    def __init__(self, repo: MentorsRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[Mentor], Exception]:
        return Err(NotImplementedError())

    async def get(self, mentor_id: str) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def create(self, mentor: Mentor) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def update(self, mentor_id: str, params: UpdateMentorParams) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())

    async def delete(self, mentor_id: str) -> Result[Mentor, Exception]:
        return Err(NotImplementedError())
