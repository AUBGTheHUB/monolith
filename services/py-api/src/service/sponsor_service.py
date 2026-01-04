from typing import List

from src.database.model.sponsor_model import Sponsor
from src.database.repository.sponsor_repository import SponsorRepository

from result import Result

class SponsorService:
    def __init__(self, repository: SponsorRepository):
        self._repository = repository

    async def create_sponsor(self, sponsor: Sponsor):
        return await self._repository.create(sponsor)

    async def get_sponsors(self) -> Result[Sponsor]:
        return await self._repository.fetch_all()