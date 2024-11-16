from asyncio import to_thread
from multiprocessing.util import get_logger
from os import getenv
from typing import Literal
from dotenv import load_dotenv

import resend
from src.service.mail_service.mail_service import MailService
from src.service.mail_service.utils import (
    load_email_participant_html_template,
    load_email_verify_participant_html_template,
)

SENDER_EMAIL = "onboarding@resend.dev"
# SENDER_EMAIL = "thehubaubg.noreply@gmail.com" # We obviously need to supply our own email here.

LOG = get_logger()
load_dotenv()


class ResendMailService(MailService):
    """Service layer responsible for the resend MailService implementation"""

    def __init__(self) -> None:
        api_key = getenv("RESEND_API_KEY")
        if not api_key:
            raise ValueError("RESEND_API_KEY environment variable is not set")
        resend.api_key = api_key
        self.client = resend

    async def send_email(
        self, receiver: str, subject: str, body_content: str, content_type: Literal["text", "html"] = "text"
    ):
        params: resend.Emails.SendParams = {
            "from": f"THE HUB <{SENDER_EMAIL}>",
            "to": [receiver],
            "subject": subject,
            content_type: body_content,
        }

        try:
            email: resend.Email = await to_thread(self.client.Emails.send, params)
            LOG.info(f"Email sent successfully: {email}")
            return email
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}") from e

    async def send_participant_successful_registration_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        invite_link: str,
    ) -> None:
        try:
            body_html = load_email_participant_html_template(participant, team_name, invite_link)
        except ValueError as e:
            raise ValueError(f"Error loading the HTML template: {str(e)}") from e

        try:
            return await self.send_email(
                receiver=receiver, subject=subject, body_content=body_html, content_type="html"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}") from e

    async def send_participant_verification_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        confirmation_link: str,
    ) -> None:
        try:
            body_html = load_email_verify_participant_html_template(participant, team_name, confirmation_link)
        except ValueError as e:
            raise ValueError(f"Failed to load email template: {str(e)}")

        try:
            return await self.send_email(
                receiver=receiver, subject=subject, body_content=body_html, content_type="html"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send participant confirmation email: {str(e)}") from e
