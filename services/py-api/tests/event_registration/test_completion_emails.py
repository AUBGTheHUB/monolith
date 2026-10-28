import pytest
from fastapi import BackgroundTasks
from result import Ok

from src.service.event_registration_mail_service import (
    EventRegistrationMailService,
)


class FakeMailClient:

    def __init__(self, fail=False):
        self.fail = fail
        self.sent = []

    def send_email(
        self,
        sender,
        receiver,
        subject,
        body_content,
        content_type="text",
    ):
        if self.fail:
            raise RuntimeError("Email provider unavailable")

        self.sent.append(
            {
                "receiver": receiver,
                "subject": subject,
                "body": body_content,
            }
        )


class FakeTeamsRepository:

    def __init__(self):
        self.marked_sent = False

    async def mark_completion_email_sent(self, code):
        self.marked_sent = True
        return Ok(True)


@pytest.mark.asyncio
async def test_completion_email_sent_and_recorded():
    mail_client = FakeMailClient()
    teams_repository = FakeTeamsRepository()

    service = EventRegistrationMailService(
        client=mail_client,
        teams_repository=teams_repository,
    )

    tasks = BackgroundTasks()

    service.queue_team_completion_email(
        leader_email="leader@example.com",
        team_name="Night Owls",
        team_code="ABC12345",
        background_tasks=tasks,
    )

    assert mail_client.sent == []

    await tasks()

    assert len(mail_client.sent) == 1
    assert mail_client.sent[0]["receiver"] == "leader@example.com"
    assert teams_repository.marked_sent is True


@pytest.mark.asyncio
async def test_failed_email_is_not_marked_sent():
    mail_client = FakeMailClient(fail=True)
    teams_repository = FakeTeamsRepository()

    service = EventRegistrationMailService(
        client=mail_client,
        teams_repository=teams_repository,
    )

    tasks = BackgroundTasks()

    service.queue_team_completion_email(
        leader_email="leader@example.com",
        team_name="Night Owls",
        team_code="ABC12345",
        background_tasks=tasks,
    )

    await tasks()

    assert mail_client.sent == []
    assert teams_repository.marked_sent is False
