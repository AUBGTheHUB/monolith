from src.service.admin.past_events_service import PastEventsService


# Past Events Handlers
class PastEventsHandlers(BaseException):
    def __init__(self, service: PastEventsService) -> None:
        self._service = service

    async def create_past_event(self) -> None:
        raise NotImplementedError()

    async def list_past_events(self) -> None:
        raise NotImplementedError()

    async def get_past_event(self, event_id: str) -> None:
        raise NotImplementedError()

    async def update_past_event(self, event_id: str) -> None:
        raise NotImplementedError()

    async def delete_past_event(self, event_id: str) -> None:
        raise NotImplementedError()
