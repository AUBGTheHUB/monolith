from asyncio import to_thread
from multiprocessing.util import get_logger
from os import getenv
from typing import Literal, Any, Coroutine
from dotenv import load_dotenv

import resend
from result import Result, Ok, Err

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
            LOG.exception("RESEND_API_KEY environment variable is not set")
            raise ValueError("RESEND_API_KEY environment variable is not set")
        resend.api_key = api_key
        self.client = resend

    async def send_email(
        self, receiver: str, subject: str, body_content: str, content_type: Literal["text", "html"] = "text"
    ) -> Result[resend.Email, str]:
        params: resend.Emails.SendParams = {
            "from": f"THE HUB <{SENDER_EMAIL}>",
            "to": [receiver],
            "subject": subject,
            content_type: body_content,
        }

        try:
            email: resend.Email = await to_thread(self.client.Emails.send, params)
            LOG.info(f"Email sent successfully: {email}")
            return Ok(email)
        except Exception as e:
            LOG.exception(f"Failed to send email: {str(e)}")
            return Err(f"Failed to send email: {str(e)}")

    async def send_participant_successful_registration_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        invite_link: str,
    ) -> Result[resend.Email, str]:
        try:
            body_html = load_email_participant_html_template(participant, team_name, invite_link)
        except ValueError as e:
            LOG.exception(f"Error loading the HTML template: {str(e)}")
            return Err(f"Error loading the HTML template: {str(e)}")

        send_result = await self.send_email(
            receiver=receiver, subject=subject, body_content=body_html, content_type="html"
        )

        if send_result.is_ok():
            return send_result
        else:
            return Err(f"Failed to send participant registration email: {send_result.err()}")

    async def send_participant_verification_email(
            self,
            receiver: str,
            subject: str,
            participant: str,
            team_name: str,
            confirmation_link: str,
    ) -> Result[resend.Email, str]:
        try:
            body_html = load_email_verify_participant_html_template(participant, team_name, confirmation_link)
        except ValueError as e:
            LOG.exception(f"Failed to load email template: {str(e)}")
            return Err(f"Failed to load email template: {str(e)}")

        send_result = await self.send_email(
            receiver=receiver, subject=subject, body_content=body_html, content_type="html"
        )

        if send_result.is_ok():
            return send_result
        else:
            return Err(f"Failed to send participant verification email: {send_result.err()}")
