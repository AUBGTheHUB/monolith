from dataclasses import dataclass
from src.server.handlers.admin.hub_members_handlers import HubMembersHandlers
from src.server.handlers.admin.judges_handlers import JudgesHandlers
from src.server.handlers.admin.mentor_handlers import MentorsHandlers
from src.server.handlers.admin.past_events_handlers import PastEventsHandlers
from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers


@dataclass(kw_only=True, frozen=True)
class AdminHandlers:
    sponsors_handlers: SponsorsHandlers
    mentors_handlers: MentorsHandlers
    judges_handlers: JudgesHandlers
    hub_members_handlers: HubMembersHandlers
    past_events_handlers: PastEventsHandlers
