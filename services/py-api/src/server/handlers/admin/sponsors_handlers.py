from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import HttpUrl
from result import is_err

from src.database.model.admin.sponsor_model import ALLOWED_SPONSOR_TIERS
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.admin.sponsor_schemas import SponsorResponse, SponsorsResponse
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.sponsors_service import SponsorsService


# Sponsors Handlers
class SponsorsHandlers(BaseHandler):
    def __init__(self, service: SponsorsService) -> None:
        self._service = service

    async def create_sponsor(
        self,
        name: Annotated[str, Form(...)],
        tier: Annotated[ALLOWED_SPONSOR_TIERS, Form()],
        logo: Annotated[UploadFile, Form()],
        website_url: Annotated[HttpUrl | None, Form()] = None,
    ) -> Response:
        result = await self._service.create(name=name, tier=tier, logo=logo, website_url=website_url)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=201)

    async def get_all_sponsors(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorsResponse(sponsors=result.ok_value), status_code=200)

    async def get_sponsor(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)

    async def update_sponsor(
        self,
        object_id: str,
        name: Annotated[str | None, Form(...)] = None,
        tier: Annotated[ALLOWED_SPONSOR_TIERS | None, Form()] = None,
        logo: Annotated[UploadFile | None, Form()] = None,
        website_url: Annotated[HttpUrl | None, Form()] = None,
    ) -> Response:
        result = await self._service.update(object_id, name, tier, logo, website_url)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)

    async def delete_sponsor(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)
