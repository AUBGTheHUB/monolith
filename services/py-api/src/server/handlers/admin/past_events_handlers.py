from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.past_events_service import PastEventsService


# Past Events Handlers
class PastEventsHandlers(BaseHandler):
    def __init__(self, service: PastEventsService) -> None:
        self._service = service

    async def create_past_event(self) -> Response:
        raise NotImplementedError()

    async def get_all_past_events(self) -> Response:
        raise NotImplementedError()

    async def get_past_event(self, event_id: str) -> Response:
        raise NotImplementedError()

    async def update_past_event(self, event_id: str) -> Response:
        raise NotImplementedError()

    async def delete_past_event(self, event_id: str) -> Response:
        raise NotImplementedError()
