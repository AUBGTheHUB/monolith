import pytest
from bson import ObjectId
from result import Ok, is_ok, is_err

from src.service.registration_services import assign_solo_member_to_team


class FakeTransactionManager:

    async def with_transaction(self, operation):
        return await operation(session=None)


class FakeParticipantsRepository:

    def __init__(self, *participants):
        self.participants = {participant["_id"]: participant for participant in participants}

    async def find_by_id(self, participant_id, session=None):
        return Ok(self.participants.get(participant_id))

    async def assign_solo_to_team(
        self,
        participant_id,
        team_id,
        assigned_role,
        session=None,
    ):
        participant = self.participants.get(participant_id)

        if participant is None or participant.get("team_id") is not None:
            return Ok(None)

        participant["team_id"] = team_id
        participant["assigned_role"] = assigned_role

        return Ok(participant.copy())


class FakeTeamsRepository:

    def __init__(self, team):
        self.team = team

    async def find_by_code(self, code, session=None):
        if self.team["code"] == code:
            return Ok(self.team.copy())

        return Ok(None)

    async def reserve_slot(self, code, session=None):
        if self.team["code"] != code:
            return Ok(None)

        if self.team["member_count"] >= 5:
            return Ok(None)

        self.team["member_count"] += 1

        return Ok(self.team.copy())

    async def mark_completed(self, code, session=None):
        if self.team["code"] == code and self.team["member_count"] == 5 and self.team["completed_at"] is None:
            self.team["completed_at"] = "completed"
            return Ok(self.team.copy())

        return Ok(None)


def make_team(member_count=3):
    return {
        "_id": ObjectId(),
        "code": "ABC123",
        "name": "Night Owls",
        "leader_id": ObjectId(),
        "member_count": member_count,
        "completed_at": None,
    }


def make_solo():
    return {
        "_id": ObjectId(),
        "email": "solo@example.com",
        "team_id": None,
        "is_team_leader": False,
        "assigned_role": None,
    }


@pytest.mark.asyncio
async def test_assign_solo_participant_to_team():
    team = make_team()
    solo = make_solo()

    participants = FakeParticipantsRepository(solo)
    teams = FakeTeamsRepository(team)

    result = await assign_solo_member_to_team(
        participant_id=str(solo["_id"]),
        team_code="abc123",
        assigned_role="Designer",
        participants_repository=participants,
        teams_repository=teams,
        transaction_manager=FakeTransactionManager(),
    )

    assert is_ok(result)
    assert result.ok_value["team_id"] == team["_id"]
    assert result.ok_value["assigned_role"] == "Designer"
    assert team["member_count"] == 4


@pytest.mark.asyncio
async def test_cannot_assign_to_full_team():
    team = make_team(member_count=5)
    solo = make_solo()

    result = await assign_solo_member_to_team(
        participant_id=str(solo["_id"]),
        team_code="ABC123",
        assigned_role="Designer",
        participants_repository=FakeParticipantsRepository(solo),
        teams_repository=FakeTeamsRepository(team),
        transaction_manager=FakeTransactionManager(),
    )

    assert is_err(result)
    assert team["member_count"] == 5
    assert solo["team_id"] is None


@pytest.mark.asyncio
async def test_cannot_assign_participant_twice():
    team = make_team()
    solo = make_solo()

    solo["team_id"] = ObjectId()

    result = await assign_solo_member_to_team(
        participant_id=str(solo["_id"]),
        team_code="ABC123",
        assigned_role="Designer",
        participants_repository=FakeParticipantsRepository(solo),
        teams_repository=FakeTeamsRepository(team),
        transaction_manager=FakeTransactionManager(),
    )

    assert is_err(result)
    assert team["member_count"] == 3


@pytest.mark.asyncio
async def test_assigning_fifth_member_triggers_completion():
    team = make_team(member_count=4)
    solo = make_solo()

    leader = {
        "_id": team["leader_id"],
        "email": "leader@example.com",
        "team_id": team["_id"],
        "is_team_leader": True,
    }

    notifications = []

    result = await assign_solo_member_to_team(
        participant_id=str(solo["_id"]),
        team_code="ABC123",
        assigned_role="Designer",
        participants_repository=FakeParticipantsRepository(solo, leader),
        teams_repository=FakeTeamsRepository(team),
        transaction_manager=FakeTransactionManager(),
        on_team_completed=lambda email, name, code: notifications.append((email, name, code)),
    )

    assert is_ok(result)
    assert team["member_count"] == 5
    assert team["completed_at"] is not None

    assert notifications == [("leader@example.com", "Night Owls", "ABC123")]
