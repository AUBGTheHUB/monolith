from asyncio import to_thread
from typing import Literal
from asyncio import sleep
from resend.exceptions import ResendError
from resend import Email
from os import environ
from structlog.stdlib import get_logger

import resend
from result import Result, Ok, Err
from requests.exceptions import RequestException

from database.model.participant_model import Participant
from src.service.mail_service.mail_service import MailService
from src.service.mail_service.utils import (
    load_email_participant_html_template,
    load_email_verify_participant_html_template,
)

LOG = get_logger()

SENDER_EMAIL = "onboarding@resend.dev"
MAX_RETRIES = 3
INITIAL_RETRY_DELAY_SECONDS = 1  # seconds
UNRETRYABLE_STATUS_CODES = {401, 422, 403, 400}


class ResendMailService(MailService):
    """Service layer responsible for the resend MailService implementation"""

    def __init__(self) -> None:
        api_key = environ["RESEND_API_KEY"]
        if not api_key:
            LOG.exception("RESEND_API_KEY environment variable is not set")
            raise ValueError("RESEND_API_KEY environment variable is not set")
        resend.api_key = api_key
        self.client = resend

    async def send_email(
        self, participant_email: str, subject: str, body_content: str, content_type: Literal["text", "html"] = "text"
    ) -> Result[Email, str]:
        # Prepare the email parameters
        params = {
            "from": f"THE HUB <{SENDER_EMAIL}>",
            "to": [participant_email],
            "subject": subject,
            content_type: body_content,
        }

        # Retry logic
        retry_delay = INITIAL_RETRY_DELAY_SECONDS
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Send the email asynchronously
                email = await to_thread(self.client.Emails.send, params)
                LOG.info(f"Email sent successfully: {email}")
                return Ok(email)

            except ResendError as e:
                if e.code in UNRETRYABLE_STATUS_CODES:
                    LOG.exception(f"Unretryable error occurred: {e.code} - {e.message}. Not retrying.")
                    return Err(f"Failed to send email: {e.message}")

                # handle 500 ApplicationError transient issue, retry allowed
                if e.code == "500":
                    LOG.warning(f"Application error occurred: {e.message}. Retrying after delay...")
                else:
                    LOG.warning(
                        f"Retryable error: {e.code} - {e.message}. Attempt {attempt} failed. Retrying in {retry_delay} seconds..."
                    )

            except RequestException as e:
                LOG.warning(f"Network error: {e}. Attempt {attempt} failed. Retrying in {retry_delay} seconds...")
            except Exception as e:
                LOG.warning(
                    f"Unexpected error occurred: {e}. Attempt {attempt} failed. Retrying in {retry_delay} seconds..."
                )

            # Wait before retrying
            await sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

        LOG.exception(f"Failed to send email after {MAX_RETRIES} attempts.")
        return Err(f"Failed to send email after {MAX_RETRIES} attempts.")

    async def send_participant_successful_registration_email(
        self,
        participant: Participant,
        team_name: str,
        invite_link: str,
    ) -> Result[Email, str]:
        try:
            body_html = load_email_participant_html_template(participant.name, team_name, invite_link)
        except ValueError as e:
            LOG.exception(f"Error loading the HTML template: {str(e)}")
            return Err(f"Error loading the HTML template: {str(e)}")

        send_result = await self.send_email(
            # TODO: Fix the subject
            participant_email=participant.email,
            subject="successful registration subject",
            body_content=body_html,
            content_type="html",
        )
        return send_result

    async def send_participant_verification_email(
        self,
        participant: Participant,
        team_name: str,
        confirmation_link: str,
    ) -> Result[Email, str]:
        try:
            body_html = load_email_verify_participant_html_template(participant.name, team_name, confirmation_link)
        except ValueError as e:
            LOG.exception(f"Failed to load email template: {str(e)}")
            return Err(f"Failed to load email template: {str(e)}")

        send_result = await self.send_email(
            # TODO: Fix the subject
            participant_email=participant.email,
            subject="verification email subject",
            body_content=body_html,
            content_type="html",
        )
        return send_result
