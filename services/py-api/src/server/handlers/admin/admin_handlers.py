from src.service.admin.sponsors_service import SponsorsService
from src.service.admin.mentors_service import MentorsService
from src.service.admin.judges_service import JudgesService
from src.service.admin.hub_members_service import HubMembersService
from src.service.admin.past_events_service import PastEventsService


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


# Mentors Handlers
class MentorsHandlers(BaseException):
    def __init__(self, service: MentorsService) -> None:
        self._service = service

    async def create_mentor(self) -> None:
        raise NotImplementedError()

    async def list_mentors(self) -> None:
        raise NotImplementedError()

    async def get_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()

    async def update_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()

    async def delete_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()


# Judges Handlers
class JudgesHandlers(BaseException):
    def __init__(self, service: JudgesService) -> None:
        self._service = service

    async def create_judge(self) -> None:
        raise NotImplementedError()

    async def list_judges(self) -> None:
        raise NotImplementedError()

    async def get_judge(self, judge_id: str) -> None:
        raise NotImplementedError()

    async def update_judge(self, judge_id: str) -> None:
        raise NotImplementedError()

    async def delete_judge(self, judge_id: str) -> None:
        raise NotImplementedError()


# Hub Members Handlers
class HubMembersHandlers(BaseException):
    def __init__(self, service: HubMembersService) -> None:
        self._service = service

    async def create_hub_member(self) -> None:
        raise NotImplementedError()

    async def list_hub_members(self) -> None:
        raise NotImplementedError()

    async def get_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()

    async def update_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()

    async def delete_hub_member(self, member_id: str) -> None:
        raise NotImplementedError()


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
