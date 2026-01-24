from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.sponsors_service import SponsorsService

from result import is_err

from src.database.model.admin.sponsor_model import Sponsor
from src.server.schemas.request_schemas.admin.sponsor_schemas import SponsorPostReqData, SponsorPatchReqData
from src.server.schemas.response_schemas.admin.sponsor_schemas import SponsorResponse, SponsorsResponse

# Sponsors Handlers
class SponsorsHandlers(BaseHandler):
    def __init__(self, service: SponsorsService) -> None:
        self._service = service

    async def create_sponsor(self, sponsor: SponsorPostReqData) -> Response:
        result = await self._service.create(sponsor)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=201)

    async def get_all_sponsors(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorsResponse(sponsors=result.ok_value), status_code=200)

    async def get_sponsor(self, sponsor_id: str) -> Response:
        result = await self._service.get(sponsor_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)

    async def update_sponsor(self, sponsor_id: str, sponsor_data: SponsorPatchReqData) -> Response:
        result = await self._service.update(sponsor_id, sponsor_data)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)

    async def delete_sponsor(self, sponsor_id: str) -> Response:
        result = await self._service.delete(sponsor_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(SponsorResponse(sponsor=result.ok_value), status_code=200)
