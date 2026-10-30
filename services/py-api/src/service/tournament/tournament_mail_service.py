from fastapi import BackgroundTasks
from result import Err, Ok, Result
from src.database.model.tournament_registration.tournament_participant_model import TournamentParticipant
from src.service.mail_service.utils import (
    load_email_tournament_team_registration_html_template,
    load_email_tournament_team_complete_html_template,
)
from structlog.stdlib import get_logger

from src.service.mail_service.mail_clients.base_mail_client import MailClient

LOG = get_logger()


class TournamentMailService:

    _SENDER_EMAIL = "no-reply@thehub-aubg.com"

    def __init__(self, client: MailClient) -> None:
        self._client = client

    async def send_email_with_team_code(
        self, tournament_participant: TournamentParticipant, background_tasks: BackgroundTasks, team_code: str
    ) -> Result[None, ValueError]:
        """
        Sends an email confirming the successful registration of the tournament admin participant with the generated team code.
        """
        try:
            body_html = load_email_tournament_team_registration_html_template(
                participant_name=tournament_participant.full_name, team_code=team_code
            )

        except ValueError as e:
            LOG.exception(
                "Error loading the HTML template for successful tournament team registration email",
                err=e,
                tournament_participant=tournament_participant,
                team_code=team_code,
            )
            return Err(e)

        LOG.info(
            "Sending successful tournament team registration email...",
            tournament_participant=tournament_participant.dump_as_json(),
            team_code=team_code,
        )

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=tournament_participant.email,
            subject="Welcome Aboard! See You at Play Con!",
            body_content=body_html,
            content_type="html",
        )

        return Ok(None)

    async def send_email_when_team_is_complete(
        self, tournament_participant: TournamentParticipant, team_name: str, background_tasks: BackgroundTasks
    ) -> Result[None, ValueError]:
        """
        Sends an email confirming the successful comletion of the tournament team.
        """
        try:
            body_html = load_email_tournament_team_complete_html_template(
                participant_name=tournament_participant.full_name, team_name=team_name
            )

        except ValueError as e:
            LOG.exception(
                "Error loading the HTML template for successful tournament team completion email",
                err=e,
                tournament_participant=tournament_participant,
            )
            return Err(e)

        LOG.info(
            "Sending successful tournament team completion email...",
            tournament_participant=tournament_participant.dump_as_json(),
        )

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=tournament_participant.email,
            subject="Team Complete! See You at Play Con!",
            body_content=body_html,
            content_type="html",
        )

        return Ok(None)
