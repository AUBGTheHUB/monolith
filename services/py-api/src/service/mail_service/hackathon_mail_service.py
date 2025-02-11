from fastapi import BackgroundTasks
from result import Err
from structlog.stdlib import get_logger

from src.database.model.participant_model import Participant
from src.service.mail_service.mail_client import MailClient
from src.service.mail_service.utils import (
    load_email_registration_confirmation_html_template,
    load_email_verify_participant_html_template,
)

LOG = get_logger()


class HackathonMailService:
    """
    Service layer responsible for sending verification and successful registration emails to hackathon participants
    """

    _SENDER_EMAIL = "no-reply@thehub-aubg.com"

    def __init__(self, client: MailClient) -> None:
        self._client = client

    def send_participant_verification_email(
        self,
        participant: Participant,
        verification_link: str,
        background_tasks: BackgroundTasks,
        team_name: str | None = None,
    ) -> Err[ValueError]:
        """
        Sends a verification email to admin and random participants via FastAPI BackgroundTasks

        Args:
            participant: The participant who should receive the email. Admin or random participant only, invite_link
                    participants are automatically verified.
            verification_link: The generated email verification link with appended JWT token.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
                system. It is auto-wired for us. We use background tasks as we want to send an email only once we
                have returned a response. In this way we are able to keep our response times sub-second as we don't
                wait for the email to be sent, which could take more than 2 seconds.
            team_name: Should be passed only when sending admin verification emails. If passed it will show up in the
             verification email as "Hello {participant.name}, from team {team_name}", otherwise it will be only
             "Hello {participant.name}".
        Returns:
            Err[ValueError] if there was an error generating the email body
        """
        try:
            body_html = load_email_verify_participant_html_template(participant.name, team_name, verification_link)
        except ValueError as e:
            LOG.exception("Error loading the HTML template", err=str(e))
            return Err(e)

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=participant.email,
            subject="verification email subject",  # TODO: Change before deploying to PROD
            body_content=body_html,
            content_type="html",
        )

    def send_participant_successful_registration_email(
        self,
        participant: Participant,
        background_tasks: BackgroundTasks,
        invite_link: str | None = None,
        team_name: str | None = None,
    ) -> Err[ValueError]:
        """
        Sends an email confirming the successful registration of a participant.

        Args:
            participant: The participant who should receive the email. Could be admin, random or invite_link participant.
            invite_link: The hackathon participants registration endpoint with appended JWT token. Should be passed
             only when sending emails to admin participants, as they are responsible for sharing the link with teammates.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
             system. It is auto-wired for us. We use background tasks as we want to send an email only once we
             have returned a response. In this way we are able to keep our response times sub-second as we don't
             wait for the email to be sent, which could take more than 2 seconds.
            team_name: Should be passed only when sending emails to admin or invite_link participants. If passed it will
             show up in the confirmation email as "Hello {participant.name}, from team {team_name}", otherwise it will
             be only "Hello {participant.name}".
        Returns:
            Err[ValueError] if there was an error generating the email body
        """

        try:
            body_html = load_email_registration_confirmation_html_template(participant.name, team_name, invite_link)
        except ValueError as e:
            LOG.exception("Error loading the HTML template", err=str(e))
            return Err(e)

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=participant.email,
            subject="successful registration subject",  # TODO: Change before deploying to PROD
            body_content=body_html,
            content_type="html",
        )
