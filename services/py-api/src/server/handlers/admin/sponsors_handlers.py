from src.service.admin.sponsors_service import SponsorsService


# Sponsors Handlers
class SponsorsHandlers(BaseException):
    def __init__(self, service: SponsorsService) -> None:
        self._service = service

    async def create_sponsor(self) -> None:
        raise NotImplementedError()

    async def list_sponsors(self) -> None:
        raise NotImplementedError()

    async def get_sponsor(self, sponsor_id: str) -> None:
        raise NotImplementedError()

    async def update_sponsor(self, sponsor_id: str) -> None:
        raise NotImplementedError()

    async def delete_sponsor(self, sponsor_id: str) -> None:
        raise NotImplementedError()
