from abc import ABC, abstractmethod
from time import sleep
from typing import Literal

import resend
from requests import RequestException
from resend.exceptions import ResendError
from structlog.stdlib import get_logger

from src.utils import SingletonABCMeta

LOG = get_logger()


class MailClient(ABC, metaclass=SingletonABCMeta):
    """Interface for sending email. Should be implemented by different email clients."""

    @abstractmethod
    def send_email(
        self,
        sender: str,
        receiver: str,
        subject: str,
        body_content: str,
        content_type: Literal["text", "html"] = "text",
    ) -> None:
        """
        Sends an email to the specified receiver with the provided subject and body content.
        Supports both text and HTML bodies.
        Args:
            sender: Email of the sender
            receiver: Email of receiver
            subject: Email subject line
            body_content: Body of the email, could be html or just plain text, must be specified in content_type
            content_type: Defines the type of the email body, could be "html" (for html body) or "text"
                (for a plain text body)
        Notes:
            Implementations are encouraged to implement a retry logic with an exponential backoff, based on the client
            in use.

            This method MUST NOT be called directly in an async context, as it will block the event loop. (We assume
            the HTTP calls made to send the email are NOT async. If using an async email client this interface should
            be extended.)

            Callers are encouraged to use mechanisms such as FastAPI BackgroundTasks or a TaskQueue such as Celery to
            avoid blocking the event loop when calling this method.
        """
        raise NotImplementedError()


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
            "from": f"THE HUB AUBG <{sender}>",
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
