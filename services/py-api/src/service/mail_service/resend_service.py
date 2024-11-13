import os
from typing import Optional
from dotenv import load_dotenv

import resend
from mail_service import MailService
from service.mail_service.utils import load_email_participant_html_template, load_email_verify_participant_html_template

SENDER_EMAIL = "tonymontana@thehub.com"  # We obviously need to supply our own email here.
load_dotenv()


class ResendMailService(MailService):
    def __init__(self) -> None:
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            raise ValueError("RESEND_API_KEY environment variable is not set")
        resend.api_key = api_key
        self.client = resend

    async def send_email(
        self, receiver: str, subject: str, body_text: Optional[str] = None, body_html: Optional[str] = None
    ) -> None:
        if not receiver:
            raise ValueError("Receiver email must be provided.")
        if not subject:
            raise ValueError("Subject must be provided.")

        if not body_text and not body_html:
            raise ValueError("At least one of body_text or body_html must be provided")

        params: resend.Emails.SendParams = {
            "from": f"THE HUB <{SENDER_EMAIL}>",
            "to": [receiver],
            "subject": subject,
        }

        if body_html:
            params["html"] = body_html
        elif body_text:
            params["text"] = body_text

        try:
            email = self.client.Emails.send(params)
            # TODO: I need to actually log here
            print("Email sent successfully: ", email)
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}") from e

    async def send_participant_successful_confirmation_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        invite_link: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
    ) -> None:
        try:
            body_html = load_email_participant_html_template(participant, team_name, invite_link)
        except ValueError as e:
            raise ValueError(f"Error loading the HTML template: {str(e)}") from e

        try:
            await self.send_email(receiver=receiver, subject=subject, body_html=body_html, body_text=body_text)
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}") from e

    async def send_participant_confirmation_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        confirmation_link: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
    ) -> None:
        if not receiver:
            raise ValueError("Receiver email must be provided.")
        if not subject:
            raise ValueError("Subject must be provided.")
        if not participant or not confirmation_link:
            raise ValueError("Both participant name and confirmation link must be provided.")

        try:
            body_html = load_email_verify_participant_html_template(participant, team_name, confirmation_link)
        except ValueError as e:
            raise ValueError(f"Failed to load email template: {str(e)}")

        try:
            await self.send_email(receiver=receiver, subject=subject, body_html=body_html, body_text=body_text)
        except Exception as e:
            raise RuntimeError(f"Failed to send participant confirmation email: {str(e)}") from e
