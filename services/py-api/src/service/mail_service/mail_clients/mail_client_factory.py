from enum import Enum
from typing import Callable

from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.mail_clients.resend_mail_client import resend_mail_client_provider


class MailClients(Enum):
    RESEND = 0


_mail_client_providers_map: dict[MailClients, Callable[[], MailClient]] = {
    MailClients.RESEND: resend_mail_client_provider
}


def mail_client_factory(mail_client_type: MailClients) -> MailClient:
    """A factory for returning MailClient instances"""

    provider = _mail_client_providers_map.get(mail_client_type)
    if provider is None:
        raise ValueError(f"No provider found for mail client: {mail_client_type}")

    # Call the provider to return an instance
    return provider()
