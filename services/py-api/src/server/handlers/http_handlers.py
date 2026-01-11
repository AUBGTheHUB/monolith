from dataclasses import dataclass

from src.server.handlers.admin.departments_handlers import DepartmentsHandlers
from src.server.handlers.admin.hub_members_handlers import HubMembersHandlers
from src.server.handlers.admin.judges_handlers import JudgesHandlers
from src.server.handlers.admin.mentor_handlers import MentorsHandlers
from src.server.handlers.admin.past_events_handlers import PastEventsHandlers
from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers
from src.server.handlers.auth.auth_handlers import AuthHandlers
from src.server.handlers.feature_switch_handlers import FeatureSwitchHandlers
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers


@dataclass(kw_only=True, frozen=True)
class HackathonHandlers:
    """Container for holding HTTP handlers for the Hackathon domain"""

    hackathon_management_handlers: HackathonManagementHandlers
    participant_handlers: ParticipantHandlers
    verification_handlers: VerificationHandlers


@dataclass(kw_only=True, frozen=True)
class AdminHandlers:
    """Container for holding HTTP handlers for the Admin domain"""

    sponsors_handlers: SponsorsHandlers
    mentors_handlers: MentorsHandlers
    judges_handlers: JudgesHandlers
    hub_members_handlers: HubMembersHandlers
    past_events_handlers: PastEventsHandlers


@dataclass(kw_only=True, frozen=True)
class HttpHandlersContainer:
    """Container for holding all HTTP handlers"""

    utility_handlers: UtilityHandlers
    fs_handlers: FeatureSwitchHandlers
    hackathon_management_handlers: HackathonManagementHandlers
    participant_handlers: ParticipantHandlers
    verification_handlers: VerificationHandlers
    departments_handlers: DepartmentsHandlers
    hackathon_handlers: HackathonHandlers
    admin_handlers: AdminHandlers
    auth_handlers: AuthHandlers
