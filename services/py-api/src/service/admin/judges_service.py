from result import Result, Err

from src.database.model.admin.judge_model import Judge
from src.server.schemas.admin.request_schemas.schemas import JudgePostReqData, JudgePatchReqData
from src.database.repository.admin.judges_repository import JudgesRepository


class JudgesService:
    def __init__(self, repo: JudgesRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Judge], Exception]:
        return Err(NotImplementedError())

    async def get(self, judge_id: str) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def create(self, data: JudgePostReqData) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def update(self, judge_id: str, data: JudgePatchReqData) -> Result[Judge, Exception]:
        return Err(NotImplementedError())

    async def delete(self, judge_id: str) -> Result[Judge, Exception]:
        return Err(NotImplementedError())
