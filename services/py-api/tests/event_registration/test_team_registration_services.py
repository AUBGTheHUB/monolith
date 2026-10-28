import pytest
from result import Ok, Err

from src.service.registration_services import (
    register_team_admin,
    register_team_member,
)


PARTICIPANT_DATA = {
    "full_name": "Alex Ivanov",
    "age": 20,
    "email": "alex@aubg.edu",
    "university": "AUBG",
    "location": "Blagoevgrad",
    "share_info_with_sponsors": False,
    "game_rank": "Gold",
    "primary_role": "Top",
    "alternative_role": "Mid",
}


class FakeParticipantsRepository:

    def __init__(self):
        self.participants = []

    async def find_by_email(self, email, session=None):
        for participant in self.participants:
            if participant.email == email:
                return Ok(participant.dump_as_mongo_db_document())
        return Ok(None)

    async def create(self, participant, session=None):
        self.participants.append(participant)
        return Ok(participant)


class FakeTeamsRepository:

    def __init__(self):
        self.teams = {}

    async def find_by_code(self, code, session=None):
        return Ok(self.teams.get(code))

    async def create(self, team, session=None):
        self.teams[team.code] = team.dump_as_mongo_db_document()
        return Ok(team)

    async def reserve_slot(self, code, session=None):
        team = self.teams.get(code)

        if team is None or team["member_count"] >= 5:
            return Ok(None)

        team["member_count"] += 1
        return Ok(team.copy())


class FakeTransactionManager:

    async def with_transaction(self, callback):
        return await callback(session=None)


@pytest.mark.asyncio
async def test_create_team_registers_leader():
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository()
    transactions = FakeTransactionManager()

    result = await register_team_admin(
        PARTICIPANT_DATA.copy(),
        "Night Owls",
        participants,
        teams,
        transactions,
    )

    assert isinstance(result, Ok)

    team = result.ok_value
    leader = participants.participants[0]

    assert team.name == "Night Owls"
    assert len(team.code) == 8
    assert team.member_count == 1
    assert team.leader_id == leader.id
    assert leader.team_id == team.id
    assert leader.is_team_leader is True


@pytest.mark.asyncio
async def test_member_can_join_team():
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository()
    transactions = FakeTransactionManager()

    created = await register_team_admin(
        PARTICIPANT_DATA.copy(),
        "Night Owls",
        participants,
        teams,
        transactions,
    )

    team = created.ok_value

    new_member = PARTICIPANT_DATA.copy()
    new_member["email"] = "maria@aubg.edu"
    new_member["full_name"] = "Maria Petrova"

    result = await register_team_member(
        new_member,
        team.code,
        participants,
        teams,
        transactions,
    )

    assert isinstance(result, Ok)
    assert result.ok_value.team_id == team.id
    assert result.ok_value.is_team_leader is False
    assert teams.teams[team.code]["member_count"] == 2


@pytest.mark.asyncio
async def test_invalid_team_code_is_rejected():
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository()

    result = await register_team_member(
        PARTICIPANT_DATA.copy(),
        "INVALID",
        participants,
        teams,
        FakeTransactionManager(),
    )

    assert isinstance(result, Err)
    assert len(participants.participants) == 0


@pytest.mark.asyncio
async def test_full_team_is_rejected():
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository()
    transactions = FakeTransactionManager()

    created = await register_team_admin(
        PARTICIPANT_DATA.copy(),
        "Night Owls",
        participants,
        teams,
        transactions,
    )

    team = created.ok_value
    teams.teams[team.code]["member_count"] = 5

    new_member = PARTICIPANT_DATA.copy()
    new_member["email"] = "maria@aubg.edu"

    result = await register_team_member(
        new_member,
        team.code,
        participants,
        teams,
        transactions,
    )

    assert isinstance(result, Err)
    assert len(participants.participants) == 1
    assert teams.teams[team.code]["member_count"] == 5


@pytest.mark.asyncio
async def test_duplicate_leader_registration_is_rejected():
    participants = FakeParticipantsRepository()
    teams = FakeTeamsRepository()
    transactions = FakeTransactionManager()

    await register_team_admin(
        PARTICIPANT_DATA.copy(),
        "Night Owls",
        participants,
        teams,
        transactions,
    )

    result = await register_team_admin(
        PARTICIPANT_DATA.copy(),
        "Second Team",
        participants,
        teams,
        transactions,
    )

    assert isinstance(result, Err)
    assert len(participants.participants) == 1
    assert len(teams.teams) == 1
