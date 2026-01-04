from result import Result

from src.database.model.sponsor_model import Sponsor
from src.server.handlers.base_handler import BaseHandler
from src.service.sponsor_service import SponsorService


class SponsorHandlers(BaseHandler):

    def __init__(self, service: SponsorService):
        self._service = service

    async def create(self, sponsor: Sponsor):
        return await self._service.create_sponsor(sponsor)

    async def get_all(self) -> Result:
        return await self._service.get_sponsors()
