from result import Result, Err

from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.server.schemas.request_schemas.admin.sponsor_schemas import SponsorPostReqData, SponsorPatchReqData
from src.exception import SponsorNotFoundError

class SponsorsService:
    def __init__(self, repo: SponsorsRepository) -> None:
        self._repo = repo

    async def get_all(self) -> Result[list[Sponsor], Exception]:
        return await self._repo.fetch_all()

    async def get(self, sponsor_id: str) -> Result[Sponsor, SponsorNotFoundError | Exception]:
        return await self._repo.fetch_by_id(sponsor_id)

    async def create(self, data: SponsorPostReqData) -> Result[Sponsor, Exception]:
        sponsor = Sponsor(**data.model_dump())
        return await self._repo.create(sponsor)

    async def update(self, sponsor_id: str, data: SponsorPatchReqData) -> Result[Sponsor, SponsorNotFoundError | Exception]:
        params = UpdateSponsorParams(**data.model_dump())
        return await self._repo.update(sponsor_id, params)

    async def delete(self, sponsor_id: str) -> Result[Sponsor, SponsorNotFoundError | Exception]:
        return await self._repo.delete(sponsor_id)
