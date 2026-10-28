from fastapi import BackgroundTasks
from result import is_err
from starlette.concurrency import run_in_threadpool
from structlog.stdlib import get_logger

from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)
from src.service.mail_service.mail_clients.base_mail_client import (
    MailClient,
)
from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)


LOG = get_logger()


class EventRegistrationMailService:

    _SENDER_EMAIL = "no-reply@thehub-aubg.com"

    def __init__(
        self,
        client: MailClient,
        teams_repository: TeamsRepository,
    ):
        self._client = client
        self._teams_repository = teams_repository

    def queue_team_completion_email(
        self,
        leader_email: str,
        team_name: str,
        team_code: str,
        background_tasks: BackgroundTasks,
    ) -> None:

        background_tasks.add_task(
            self._send_and_record,
            leader_email=leader_email,
            team_name=team_name,
            team_code=team_code,
        )

    async def _send_and_record(
        self,
        leader_email: str,
        team_name: str,
        team_code: str,
    ) -> None:

        try:
            await run_in_threadpool(
                self._client.send_email,
                sender=self._SENDER_EMAIL,
                receiver=leader_email,
                subject="Your Project S team is complete!",
                body_content=(
                    f"Hello!\n\n"
                    f"Your team, {team_name}, now has all five members.\n\n"
                    f"Your team code is: {team_code}\n\n"
                    f"We look forward to seeing you at the event!\n\n"
                    f"Project S"
                ),
                content_type="text",
            )

        except Exception as error:
            LOG.exception(
                "Failed to send team completion email",
                error=error,
                team_code=team_code,
            )
            return

        result = await self._teams_repository.mark_completion_email_sent(team_code)

        if is_err(result):
            LOG.error(
                "Email sent but notification status could not be saved",
                error=result.err_value,
                team_code=team_code,
            )

        elif not result.ok_value:
            LOG.warning(
                "Email sent but completion status was not updated",
                team_code=team_code,
            )

    async def queue_pending_completion_emails(
        self,
        participants_repository: ParticipantsRepository,
        background_tasks: BackgroundTasks,
        limit: int = 50,
    ) -> int:

        pending_result = await self._teams_repository.find_pending_completion_emails(limit=limit)

        if is_err(pending_result):
            raise pending_result.err_value

        queued_count = 0

        for team in pending_result.ok_value:

            leader_result = await participants_repository.find_by_id(team["leader_id"])

            if is_err(leader_result):
                LOG.error(
                    "Could not retrieve leader for pending email",
                    error=leader_result.err_value,
                    team_code=team["code"],
                )
                continue

            leader = leader_result.ok_value

            if leader is None:
                LOG.error(
                    "Leader not found for pending email",
                    team_code=team["code"],
                )
                continue

            self.queue_team_completion_email(
                leader_email=leader["email"],
                team_name=team["name"],
                team_code=team["code"],
                background_tasks=background_tasks,
            )

            queued_count += 1

        return queued_count
