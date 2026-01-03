from src.service.admin.judges_service import JudgesService


# Judges Handlers
class JudgesHandlers(BaseException):
    def __init__(self, service: JudgesService) -> None:
        self._service = service

    async def create_judge(self) -> None:
        raise NotImplementedError()

    async def list_judges(self) -> None:
        raise NotImplementedError()

    async def get_judge(self, judge_id: str) -> None:
        raise NotImplementedError()

    async def update_judge(self, judge_id: str) -> None:
        raise NotImplementedError()

    async def delete_judge(self, judge_id: str) -> None:
        raise NotImplementedError()
