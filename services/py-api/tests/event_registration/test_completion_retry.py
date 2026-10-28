import pytest

from bson import ObjectId
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from result import Ok

from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)
from src.service.event_registration_mail_service import (
    EventRegistrationMailService,
)
from src.server.routes.registration_routes import (
    register_registration_routes,
)
from src.server.utility.role_checker import RoleChecker


class FakeCursor:

    async def to_list(self, length):
        return [{"code": "ABC123"}][:length]


class FakeCollection:

    def find(self, *, filter, sort, limit):
        assert filter == {
            "completed_at": {"$ne": None},
            "completion_email_sent_at": None,
        }
        assert sort == [("completed_at", 1)]
        assert limit == 50

        return FakeCursor()


class FakeDbManager:

    def get_collection(self, name):
        return FakeCollection()


@pytest.mark.asyncio
async def test_find_pending_completion_emails():
    repository = TeamsRepository(FakeDbManager())

    result = await repository.find_pending_completion_emails()

    assert result.is_ok()
    assert result.ok_value == [{"code": "ABC123"}]


class FakeTeamsRepository:

    def __init__(self, pending_teams):
        self.pending_teams = pending_teams
        self.sent_codes = []

    async def find_pending_completion_emails(self, limit=50):
        return Ok(self.pending_teams[:limit])

    async def mark_completion_email_sent(self, code):
        self.sent_codes.append(code)
        return Ok(True)


class FakeParticipantsRepository:

    def __init__(self, leader):
        self.leader = leader

    async def find_by_id(self, participant_id):
        if self.leader and self.leader["_id"] == participant_id:
            return Ok(self.leader)

        return Ok(None)


class FakeMailClient:

    def __init__(self):
        self.receivers = []

    def send_email(
        self,
        sender,
        receiver,
        subject,
        body_content,
        content_type="text",
    ):
        self.receivers.append(receiver)


@pytest.mark.asyncio
async def test_pending_completion_email_is_retried():
    leader_id = ObjectId()

    team = {
        "code": "ABC123",
        "name": "Night Owls",
        "leader_id": leader_id,
        "member_count": 5,
        "completed_at": "completed",
        "completion_email_sent_at": None,
    }

    leader = {
        "_id": leader_id,
        "email": "leader@example.com",
    }

    teams = FakeTeamsRepository([team])
    participants = FakeParticipantsRepository(leader)
    mail_client = FakeMailClient()

    service = EventRegistrationMailService(
        client=mail_client,
        teams_repository=teams,
    )

    background_tasks = BackgroundTasks()

    queued = await service.queue_pending_completion_emails(
        participants_repository=participants,
        background_tasks=background_tasks,
    )

    assert queued == 1

    await background_tasks()

    assert mail_client.receivers == ["leader@example.com"]
    assert teams.sent_codes == ["ABC123"]


@pytest.mark.asyncio
async def test_missing_leader_does_not_queue_email():
    team = {
        "code": "ABC123",
        "name": "Night Owls",
        "leader_id": ObjectId(),
        "member_count": 5,
        "completed_at": "completed",
        "completion_email_sent_at": None,
    }

    teams = FakeTeamsRepository([team])
    mail_client = FakeMailClient()

    service = EventRegistrationMailService(
        client=mail_client,
        teams_repository=teams,
    )

    background_tasks = BackgroundTasks()

    queued = await service.queue_pending_completion_emails(
        participants_repository=FakeParticipantsRepository(None),
        background_tasks=background_tasks,
    )

    assert queued == 0
    assert len(background_tasks.tasks) == 0
    assert mail_client.receivers == []


class FakeRegistrationHandlers:

    def __init__(self):
        self.retry_calls = 0

    async def retry_completion_emails_handler(self, background_tasks):
        self.retry_calls += 1
        return {
            "message": "Pending completion emails queued",
            "queued": 1,
        }


def test_retry_endpoint_requires_board_authorization():
    app = FastAPI()
    handlers = FakeRegistrationHandlers()

    app.include_router(register_registration_routes(handlers))

    route = next(
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/registration/admin/retry-completion-emails"
    )

    checker = next(
        dependency.call for dependency in route.dependant.dependencies if isinstance(dependency.call, RoleChecker)
    )

    async def deny_access():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides[checker] = deny_access

    with TestClient(app) as client:
        response = client.post("/registration/admin/retry-completion-emails")

    assert response.status_code == 403
    assert handlers.retry_calls == 0
