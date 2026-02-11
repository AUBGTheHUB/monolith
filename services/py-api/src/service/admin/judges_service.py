from result import Result

from src.database.model.admin.judge_model import Judge, UpdateJudgeParams
from src.database.repository.admin.judges_repository import JudgesRepository
from src.exception import JudgeNotFoundError
from src.server.schemas.request_schemas.admin.judge_schemas import JudgePostReqData, JudgePatchReqData


class JudgesService:
    def __init__(self, repo: JudgesRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Judge], Exception]:
        return await self._repo.fetch_all()

    async def get(self, judge_id: str) -> Result[Judge, JudgeNotFoundError | Exception]:
        return await self._repo.fetch_by_id(judge_id)

    async def create(self, data: JudgePostReqData) -> Result[Judge, Exception]:
        judge = Judge(**data.model_dump())
        return await self._repo.create(judge)

    async def update(self, judge_id: str, data: JudgePatchReqData) -> Result[Judge, Exception]:
        params = UpdateJudgeParams(**data.model_dump())
        return await self._repo.update(judge_id, params)

    async def delete(self, judge_id: str) -> Result[Judge, Exception]:
        return await self._repo.delete(judge_id)
