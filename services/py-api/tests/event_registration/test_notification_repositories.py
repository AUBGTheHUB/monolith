from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from bson import ObjectId

from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)

from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)


class FakeDbManager:

    def __init__(self, collection):
        self.collection = collection

    def get_collection(self, name):
        return self.collection


class FakeParticipantsCollection:

    def __init__(self):
        self.participant_id = ObjectId()

    async def find_one(self, filter, session=None):
        if filter["_id"] == self.participant_id:
            return {
                "_id": self.participant_id,
                "email": "leader@example.com",
                "full_name": "Team Leader",
            }

        return None


@pytest.mark.asyncio
async def test_find_participant_by_id():
    collection = FakeParticipantsCollection()
    repository = ParticipantsRepository(FakeDbManager(collection))

    result = await repository.find_by_id(collection.participant_id)

    assert result.is_ok()
    assert result.ok_value["email"] == "leader@example.com"


@pytest.mark.asyncio
async def test_find_participant_with_unknown_id():
    collection = FakeParticipantsCollection()
    repository = ParticipantsRepository(FakeDbManager(collection))

    result = await repository.find_by_id(ObjectId())

    assert result.is_ok()
    assert result.ok_value is None


class FakeTeamsCollection:

    def __init__(self, completed):
        self.document = {
            "code": "ABC12345",
            "completed_at": (datetime.now(timezone.utc) if completed else None),
            "completion_email_sent_at": None,
        }

    async def update_one(self, filter, update, session=None):
        if self.document["code"] != filter["code"]:
            return SimpleNamespace(modified_count=0)

        if self.document["completed_at"] is None:
            return SimpleNamespace(modified_count=0)

        if self.document["completion_email_sent_at"] is not None:
            return SimpleNamespace(modified_count=0)

        self.document["completion_email_sent_at"] = update["$set"]["completion_email_sent_at"]

        return SimpleNamespace(modified_count=1)


@pytest.mark.asyncio
async def test_completion_email_can_be_marked_sent_once():
    collection = FakeTeamsCollection(completed=True)
    repository = TeamsRepository(FakeDbManager(collection))

    first = await repository.mark_completion_email_sent("ABC12345")
    second = await repository.mark_completion_email_sent("ABC12345")

    assert first.is_ok()
    assert first.ok_value is True

    assert second.is_ok()
    assert second.ok_value is False

    assert collection.document["completion_email_sent_at"] is not None


@pytest.mark.asyncio
async def test_email_cannot_be_marked_sent_for_incomplete_team():
    collection = FakeTeamsCollection(completed=False)
    repository = TeamsRepository(FakeDbManager(collection))

    result = await repository.mark_completion_email_sent("ABC12345")

    assert result.is_ok()
    assert result.ok_value is False
    assert collection.document["completion_email_sent_at"] is None
