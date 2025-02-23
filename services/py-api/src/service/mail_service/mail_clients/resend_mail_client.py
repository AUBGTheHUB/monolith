from time import sleep
from typing import Literal

import resend
from requests import RequestException
from resend.exceptions import ResendError
from structlog.stdlib import get_logger

from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.utils import singleton

LOG = get_logger()


class ResendMailClient(MailClient):
    _MAX_RETRIES = 3
    _INITIAL_RETRY_DELAY_SECONDS = 1
    _UNRETRYABLE_STATUS_CODES = {401, 422, 403, 400}

    def __init__(self) -> None:
        self._client = resend.Emails

    def send_email(
        self,
        sender: str,
        receiver: str,
        subject: str,
        body_content: str,
        content_type: Literal["text", "html"] = "text",
    ) -> None:
        # Prepare the email parameters
        params = {
            "from": f"THE HUB <{sender}>",
            "to": [receiver],
            "subject": subject,
            content_type: body_content,
        }

        # Retry logic
        retry_delay = self._INITIAL_RETRY_DELAY_SECONDS
        for attempt in range(1, self._MAX_RETRIES + 1):
            try:
                # As this method is executed in the background, and we return None there is no point in using the value
                _ = self._client.send(params)
                return
            except ResendError as e:
                if e.code in self._UNRETRYABLE_STATUS_CODES:
                    LOG.exception(f"Unretryable error occurred while sending email via Resend: {e.code} - {e.message}")
                    return

                # handle 500 ApplicationError transient issue and Rate limit.
                if e.code >= 500 or e.code == 429:
                    LOG.warning(
                        f"Retryable error when sending email via Resend: {e.code} - {e.message}. Attempt {attempt} "
                        f"failed. Retrying in {retry_delay} seconds..."
                    )
            except RequestException as e:
                LOG.warning(
                    f"Network error when sending email: {e}. Attempt {attempt} failed. Retrying in "
                    f"{retry_delay} seconds..."
                )
            except Exception as e:
                LOG.exception(
                    f"Unexpected error occurred: {e}. Attempt {attempt} failed. Retrying in {retry_delay} seconds..."
                )

            # Wait before retrying
            sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

        LOG.exception(f"Failed to send email via Resend after {self._MAX_RETRIES} attempts.")
        # TODO: Add sending of Discord Webhook for alert purposes


@singleton
def resend_mail_client_provider() -> ResendMailClient:
    """
    Returns:
         A preconfigured Singleton ResendMailClient instance.
    """
    return ResendMailClient()
