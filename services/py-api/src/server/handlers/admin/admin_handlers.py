from dataclasses import dataclass
from fastapi import HTTPException

from src.service.admin.sponsors_service import SponsorsService
from src.service.admin.mentors_service import MentorsService
from src.service.admin.judges_service import JudgesService
from src.service.admin.team_members_service import TeamMembersService
from src.service.admin.past_events_service import PastEventsService


def _not_implemented() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@dataclass(kw_only=True, frozen=True)
class AdminHandlers:
    sponsors_service: SponsorsService
    mentors_service: MentorsService
    judges_service: JudgesService
    team_members_service: TeamMembersService
    past_events_service: PastEventsService

    # Sponsors
    async def list_sponsors(self) -> None:
        _not_implemented()

    async def get_sponsor(self, sponsor_id: str) -> None:
        _not_implemented()

    async def create_sponsor(self) -> None:
        _not_implemented()

    async def update_sponsor(self, sponsor_id: str) -> None:
        _not_implemented()

    async def delete_sponsor(self, sponsor_id: str) -> None:
        _not_implemented()

    # Mentors
    async def list_mentors(self) -> None:
        _not_implemented()

    async def get_mentor(self, mentor_id: str) -> None:
        _not_implemented()

    async def create_mentor(self) -> None:
        _not_implemented()

    async def update_mentor(self, mentor_id: str) -> None:
        _not_implemented()

    async def delete_mentor(self, mentor_id: str) -> None:
        _not_implemented()

    # Judges
    async def list_judges(self) -> None:
        _not_implemented()

    async def get_judge(self, judge_id: str) -> None:
        _not_implemented()

    async def create_judge(self) -> None:
        _not_implemented()

    async def update_judge(self, judge_id: str) -> None:
        _not_implemented()

    async def delete_judge(self, judge_id: str) -> None:
        _not_implemented()

    # Team Members
    async def list_team_members(self) -> None:
        _not_implemented()

    async def get_team_member(self, member_id: str) -> None:
        _not_implemented()

    async def create_team_member(self) -> None:
        _not_implemented()

    async def update_team_member(self, member_id: str) -> None:
        _not_implemented()

    async def delete_team_member(self, member_id: str) -> None:
        _not_implemented()

    # Past Events
    async def list_past_events(self) -> None:
        _not_implemented()

    async def get_past_event(self, event_id: str) -> None:
        _not_implemented()

    async def create_past_event(self) -> None:
        _not_implemented()

    async def update_past_event(self, event_id: str) -> None:
        _not_implemented()

    async def delete_past_event(self, event_id: str) -> None:
        _not_implemented()
