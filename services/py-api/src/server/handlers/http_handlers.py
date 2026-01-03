from dataclasses import dataclass

from src.server.handlers.admin_panel.authentication_handler import AuthenticationHandlers
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers


@dataclass(kw_only=True, frozen=True)
class HttpHandlersContainer:
    """Container for holding all HTTP handlers"""

    utility_handlers: UtilityHandlers
    fs_handlers: FeatureSwitchHandler
    hackathon_management_handlers: HackathonManagementHandlers
    participant_handlers: ParticipantHandlers
    verification_handlers: VerificationHandlers
    authentication_handlers: AuthenticationHandlers
