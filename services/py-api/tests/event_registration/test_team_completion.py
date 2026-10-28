from datetime import datetime, timezone

import pytest
from bson import ObjectId
from result import Ok

from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)
from src.service.registration_services import register_team_member


class FakeCollection:

    def __init__(self, member_count):
        self.document = {
            "code": "ABC12345",
            "member_count": member_count,
            "completed_at": None,
        }

    async def find_one_and_update(
        self,
        *,
        filter,
        update,
        return_document,
        session,
    ):
        if filter["code"] != self.document["code"]:
            return None

        if filter["member_count"] != self.document["member_count"]:
            return None

        if self.document["completed_at"] is not None:
            return None

        self.document["completed_at"] = update["$set"]["completed_at"]

        return self.document.copy()


class FakeDbManager:

    def __init__(self, collection):
        self.collection = collection

    def get_collection(self, name):
        return self.collection


@pytest.mark.asyncio
async def test_team_can_be_marked_complete_at_five_members():
    collection = FakeCollection(member_count=5)
    repository = TeamsRepository(FakeDbManager(collection))

    result = await repository.mark_completed("ABC12345")

    assert result.is_ok()
    assert result.ok_value is not None
    assert isinstance(result.ok_value["completed_at"], datetime)


@pytest.mark.asyncio
async def test_team_completion_is_only_recorded_once():
    collection = FakeCollection(member_count=5)
    repository = TeamsRepository(FakeDbManager(collection))

    first = await repository.mark_completed("ABC12345")
    second = await repository.mark_completed("ABC12345")

    assert first.ok_value is not None
    assert second.ok_value is None


class FakeParticipantsRepository:

    def __init__(self):
        self.saved_participant = None

    async def find_by_email(self, email, session=None):
        return Ok(None)

    async def create(self, participant, session=None):
        self.saved_participant = participant
        return Ok(participant)


class FakeTeamsRepository:

    def __init__(self, member_count):
        self.member_count = member_count
        self.team_id = ObjectId()
        self.completed = False

    async def reserve_slot(self, code, session=None):
        return Ok(
            {
                "_id": self.team_id,
                "code": code,
                "member_count": self.member_count,
            }
        )

    async def mark_completed(self, code, session=None):
        self.completed = True

        return Ok(
            {
                "code": code,
                "completed_at": datetime.now(timezone.utc),
            }
        )


class FakeTransactionManager:

    async def with_transaction(self, operation):
        return await operation(session=None)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "member_count, expected_completion",
    [
        (4, False),
        (5, True),
    ],
)
async def test_registration_completes_team_only_at_five(
    member_count,
    expected_completion,
):
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository(member_count)

    participant_data = {
        "full_name": "Jane Smith",
        "age": 20,
        "email": "jane@example.com",
        "university": "AUBG",
        "location": "Blagoevgrad",
        "share_info_with_sponsors": False,
        "game_rank": "Gold",
        "primary_role": "Support",
        "alternative_role": "Mid",
    }

    result = await register_team_member(
        participant_data=participant_data,
        team_code="ABC12345",
        participants_repository=participants,
        teams_repository=teams,
        transaction_manager=FakeTransactionManager(),
    )

    assert result.is_ok()
    assert teams.completed == expected_completion
    assert participants.saved_participant.team_id == teams.team_id
