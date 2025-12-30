from result import Result, Err

from src.database.model.admin.sponsor_model import Sponsor
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.server.schemas.admin.request_schemas.schemas import SponsorPostReqData
from src.server.schemas.admin.request_schemas.schemas import SponsorPatchReqData


class SponsorsService:
    def __init__(self, repo: SponsorsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Sponsor], Exception]:
        return Err(NotImplementedError())

    async def get(self, sponsor_id: str) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def create(self, data: SponsorPostReqData) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def update(self, sponsor_id: str, data: SponsorPatchReqData) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def delete(self, sponsor_id: str) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())
