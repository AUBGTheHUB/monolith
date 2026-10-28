import pytest
from bson import ObjectId
from result import Ok

from src.database.model.event_registration.team_model import Team
from src.database.repository.event_registration.teams_repository import TeamsRepository


class FakeCollection:
    def __init__(self):
        self.documents = []

    async def insert_one(self, document, session=None):
        self.documents.append(document)


class FakeDbManager:
    def __init__(self):
        self.collection = FakeCollection()

    def get_collection(self, name):
        assert name == "event_registration_teams"
        return self.collection


@pytest.mark.asyncio
async def test_create_team():
    db_manager = FakeDbManager()
    repository = TeamsRepository(db_manager)

    team = Team(
        name="Night Owls",
        code="ABC123",
        leader_id=str(ObjectId()),
    )

    result = await repository.create(team)

    assert isinstance(result, Ok)
    assert len(db_manager.collection.documents) == 1

    saved_team = db_manager.collection.documents[0]

    assert saved_team["name"] == "Night Owls"
    assert saved_team["code"] == "ABC123"
    assert saved_team["member_count"] == 1
