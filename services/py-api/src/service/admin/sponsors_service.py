from fastapi import UploadFile
from pydantic import HttpUrl
from result import Result

from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams, ALLOWED_SPONSOR_TIERS
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.exception import SponsorNotFoundError
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class SponsorsService:
    def __init__(self, repo: SponsorsRepository, image_storing_service: ImageStoringService) -> None:
        self._repo = repo
        self._image_storing_service = image_storing_service

    async def get_all(self) -> Result[list[Sponsor], Exception]:
        return await self._repo.fetch_all()

    async def get(self, sponsor_id: str) -> Result[Sponsor, SponsorNotFoundError | Exception]:
        return await self._repo.fetch_by_id(sponsor_id)

    async def create(
        self,
        name: str,
        tier: ALLOWED_SPONSOR_TIERS,
        logo: UploadFile,
        website_url: HttpUrl | None = None,
    ) -> Result[Sponsor, Exception]:
        sponsor = Sponsor(name=name, tier=tier, logo_url="", website_url=str(website_url))
        logo_url = await self._image_storing_service.upload_image(file=logo, file_name=f"sponsors/{str(sponsor.id)}")
        sponsor.logo_url = str(logo_url)
        return await self._repo.create(sponsor)

    async def update(
        self,
        sponsor_id: str,
        name: str | None = None,
        tier: ALLOWED_SPONSOR_TIERS | None = None,
        logo: UploadFile | None = None,
        website_url: HttpUrl | None = None,
    ) -> Result[Sponsor, SponsorNotFoundError | Exception]:

        if logo is not None:
            logo_url = await self._image_storing_service.upload_image(
                file=logo, file_name=f"sponsors/{str(sponsor_id)}"
            )
        else:
            logo_url = None

        params = UpdateSponsorParams(name=name, tier=tier, logo_url=logo_url, website_url=website_url)
        return await self._repo.update(sponsor_id, params)

    async def delete(self, sponsor_id: str) -> Result[Sponsor, SponsorNotFoundError | Exception]:
        result = await self._repo.delete(sponsor_id)

        if result.is_ok():
            self._image_storing_service.delete_image(f"sponsors/{sponsor_id}")

        return result
