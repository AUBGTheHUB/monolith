from result import Result, Err

from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.repository.admin.judges_repository import JudgesRepository


class JudgesService:
    def __init__(self, repo: JudgesRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[Judge], Exception]:
        return Err(NotImplementedError())

    async def get(self, judge_id: str) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def create(self, judge: Judge) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def update(self, judge_id: str, params: UpdateJudgeParams) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def delete(self, judge_id: str) -> Result[Judge, Exception]:
        return Err(NotImplementedError())
