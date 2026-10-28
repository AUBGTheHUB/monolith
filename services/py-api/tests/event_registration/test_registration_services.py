import pytest
from result import Ok, Err

from src.service.registration_services import (
    generate_team_code,
    register_solo_member,
)


VALID_PARTICIPANT = {
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

    def __init__(self, existing=None):
        self.existing = existing
        self.saved = None

    async def find_by_email(self, email):
        return Ok(self.existing)

    async def create(self, participant, session=None):
        self.saved = participant
        return Ok(participant)


def test_generate_team_code():
    code = generate_team_code()

    assert len(code) == 8
    assert code.isalnum()
    assert code.isupper()


@pytest.mark.asyncio
async def test_register_solo_member():
    repository = FakeParticipantsRepository()

    result = await register_solo_member(
        VALID_PARTICIPANT.copy(),
        repository,
    )

    assert isinstance(result, Ok)
    assert repository.saved is not None
    assert repository.saved.full_name == "Alex Ivanov"
    assert repository.saved.team_id is None
    assert repository.saved.is_team_leader is False


@pytest.mark.asyncio
async def test_cannot_register_same_email_twice():
    repository = FakeParticipantsRepository(existing={"email": "alex@aubg.edu"})

    result = await register_solo_member(
        VALID_PARTICIPANT.copy(),
        repository,
    )

    assert isinstance(result, Err)
    assert repository.saved is None


@pytest.mark.asyncio
async def test_solo_registration_normalizes_email():
    repository = FakeParticipantsRepository()

    data = VALID_PARTICIPANT.copy()
    data["email"] = "Alex@AUBG.EDU"

    result = await register_solo_member(data, repository)

    assert isinstance(result, Ok)
    assert repository.saved.email == "alex@aubg.edu"
