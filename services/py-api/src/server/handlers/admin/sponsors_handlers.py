from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.sponsors_service import SponsorsService


# Sponsors Handlers
class SponsorsHandlers(BaseHandler):
    def __init__(self, service: SponsorsService) -> None:
        self._service = service

    async def create_sponsor(self) -> Response:
        raise NotImplementedError()

    async def get_all_sponsors(self) -> Response:
        raise NotImplementedError()

    async def get_sponsor(self, sponsor_id: str) -> Response:
        raise NotImplementedError()

    async def update_sponsor(self, sponsor_id: str) -> Response:
        raise NotImplementedError()

    async def delete_sponsor(self, sponsor_id: str) -> Response:
        raise NotImplementedError()
