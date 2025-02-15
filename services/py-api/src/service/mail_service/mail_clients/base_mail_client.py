from abc import ABC, abstractmethod
from typing import Literal


class MailClient(ABC):
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
