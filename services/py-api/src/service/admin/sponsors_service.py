from result import Result, Err

from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.repository.admin.sponsors_repository import SponsorsRepository


class SponsorsService:
    def __init__(self, repo: SponsorsRepository) -> None:
        self._repo = repo

    async def list(self) -> Result[list[Sponsor], Exception]:
        return Err(NotImplementedError())

    async def get(self, sponsor_id: str) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def create(self, sponsor: Sponsor) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def update(self, sponsor_id: str, params: UpdateSponsorParams) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())

    async def delete(self, sponsor_id: str) -> Result[Sponsor, Exception]:
        return Err(NotImplementedError())
