from enum import Enum
from typing import Dict, Callable, Annotated

from fastapi import Depends

from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.mail_clients.resend_mail_client import resend_mail_client_provider


class MailClients(Enum):
    RESEND = 0


_mail_client_providers_map: Dict[MailClients, Callable[[], MailClient]] = {
    MailClients.RESEND: resend_mail_client_provider
}


def mail_client_providers_factory(mail_client_type: MailClients) -> Callable[[], MailClient]:
    """A factory for returning a mail client "provider" function based on a given mail client type. When using it with
    the FastAPI Dependency Injection system it should be passes to the ``fastapi.Depends`` like this::
        # mail_client_providers_factory(MailClients.RESEND) will be evaluated first before it's passed to Depends
        MailClientDep = Annotated[MailClient, Depends(mail_client_providers_factory(MailClients.RESEND))]
    """

    provider = _mail_client_providers_map.get(mail_client_type)
    if provider is None:
        raise ValueError(f"No provider found for mail client: {mail_client_type}")

    return provider


# https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies
# If needed we would easily swap the underlying MailClient impl, by passing a different value to the factory
MailClientDep = Annotated[MailClient, Depends(mail_client_providers_factory(MailClients.RESEND))]
"""FastAPI dependency for automatically injecting a MailClient instance into consumers"""
