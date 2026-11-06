from fastapi import BackgroundTasks
from resend import Attachment
from result import Err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.event.attendee_model import Attendee
from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.utils import load_email_attendee_ticket_html_template

LOG = get_logger()


class MailService:

    _SENDER_EMAIL = "no-reply@thehub-aubg.com"

    def __init__(self, client: MailClient) -> None:
        self._client = client

    async def send_email_with_ticket(
        self, attendee: Attendee, pass_data: str, background_tasks: BackgroundTasks
    ) -> Result[None, ValueError]:
        """
        Sends an email confirming the successful registration of the tournament admin participant with the generated team code.
        """
        try:
            body_html = load_email_attendee_ticket_html_template(name=attendee.name)

        except ValueError as e:
            LOG.exception(
                "Error loading the HTML template for successful tournament team registration email",
                err=e,
                attendee=attendee,
            )
            return Err(e)

        LOG.info(
            "Sending successful tournament team registration email...", tournament_participant=attendee.dump_as_json()
        )

        pass_attachment: Attachment = {
            "filename": "Ticket.pkpass",
            "content": pass_data,
            "content_type": "application/vnd.apple.pkpass",
        }

        background_tasks.add_task(
            self._client.send_email_with_attachments,
            sender=self._SENDER_EMAIL,
            receiver=attendee.email,
            subject="Welcome Aboard! See You at Play Con!",
            body_content=body_html,
            attachments=[pass_attachment],
        )

        return Ok(None)
