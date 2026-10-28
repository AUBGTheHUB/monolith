import pytest
from result import Ok

from src.database.mongo.collections.event_registration_collections import (
    PARTICIPANTS_COLLECTION,
    TEAMS_COLLECTION,
)
from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)
from src.database.repository.event_registration.teams_repository import (
    TeamsRepository,
)


class FakeCollection:
    def __init__(self, documents):
        self.documents = documents

    async def find_one(self, filter, session=None):
        for document in self.documents:
            if all(document.get(key) == value for key, value in filter.items()):
                return document.copy()
        return None

    async def find_one_and_update(self, filter, update, session=None, return_document=None):
        for document in self.documents:
            if (
                document.get("code") == filter["code"]
                and document.get("member_count", 0) < filter["member_count"]["$lt"]
            ):
                document["member_count"] += update["$inc"]["member_count"]
                return document.copy()

        return None


class FakeDbManager:
    def __init__(self, collection_name, documents):
        self.collection_name = collection_name
        self.collection = FakeCollection(documents)

    def get_collection(self, name):
        assert name == self.collection_name
        return self.collection


# ----------------------------------
# Team lookup
# ----------------------------------


@pytest.mark.asyncio
async def test_find_team_by_code():
    db = FakeDbManager(
        TEAMS_COLLECTION,
        [{"code": "ABC123", "name": "Night Owls", "member_count": 3}],
    )

    repository = TeamsRepository(db)

    result = await repository.find_by_code("ABC123")

    assert isinstance(result, Ok)
    assert result.ok_value["name"] == "Night Owls"


@pytest.mark.asyncio
async def test_find_team_with_invalid_code():
    db = FakeDbManager(TEAMS_COLLECTION, [])

    repository = TeamsRepository(db)

    result = await repository.find_by_code("INVALID")

    assert isinstance(result, Ok)
    assert result.ok_value is None


# ----------------------------------
# Participant lookup
# ----------------------------------


@pytest.mark.asyncio
async def test_find_participant_by_email():
    db = FakeDbManager(
        PARTICIPANTS_COLLECTION,
        [{"email": "test@example.com", "full_name": "Test User"}],
    )

    repository = ParticipantsRepository(db)

    result = await repository.find_by_email("test@example.com")

    assert isinstance(result, Ok)
    assert result.ok_value["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_find_participant_with_unknown_email():
    db = FakeDbManager(PARTICIPANTS_COLLECTION, [])

    repository = ParticipantsRepository(db)

    result = await repository.find_by_email("unknown@example.com")

    assert isinstance(result, Ok)
    assert result.ok_value is None


# ----------------------------------
# Team capacity
# ----------------------------------


@pytest.mark.asyncio
async def test_reserve_last_team_slot():
    db = FakeDbManager(
        TEAMS_COLLECTION,
        [{"code": "ABC123", "name": "Night Owls", "member_count": 4}],
    )

    repository = TeamsRepository(db)

    result = await repository.reserve_slot("ABC123")

    assert isinstance(result, Ok)
    assert result.ok_value["member_count"] == 5
    assert db.collection.documents[0]["member_count"] == 5


@pytest.mark.asyncio
async def test_cannot_reserve_slot_in_full_team():
    db = FakeDbManager(
        TEAMS_COLLECTION,
        [{"code": "ABC123", "name": "Night Owls", "member_count": 5}],
    )

    repository = TeamsRepository(db)

    result = await repository.reserve_slot("ABC123")

    assert isinstance(result, Ok)
    assert result.ok_value is None
    assert db.collection.documents[0]["member_count"] == 5
