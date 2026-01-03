from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.handlers.admin.admin_handlers import (
    SponsorsHandlers,
    MentorsHandlers,
    JudgesHandlers,
    HubMembersHandlers,
    PastEventsHandlers,
)
from src.server.handlers.base_handler import BaseHandler


class HttpHandlersContainer(BaseHandler):
    """DTO-like container for holding all HTTP handlers"""

    def __init__(
        self,
        *,
        utility_handlers: UtilityHandlers,
        fs_handlers: FeatureSwitchHandler,
        hackathon_management_handlers: HackathonManagementHandlers,
        participant_handlers: ParticipantHandlers,
        verification_handlers: VerificationHandlers,
        sponsors_handlers: SponsorsHandlers,
        mentors_handlers: MentorsHandlers,
        judges_handlers: JudgesHandlers,
        hub_members_handlers: HubMembersHandlers,
        past_events_handlers: PastEventsHandlers,
    ) -> None:
        self.utility_handlers = utility_handlers
        self.fs_handlers = fs_handlers
        self.hackathon_management_handlers = hackathon_management_handlers
        self.participant_handlers = participant_handlers
        self.verification_handlers = verification_handlers
        self.sponsors_handlers = sponsors_handlers
        self.mentors_handlers = mentors_handlers
        self.judges_handlers = judges_handlers
        self.hub_members_handlers = hub_members_handlers
        self.past_events_handlers = past_events_handlers
