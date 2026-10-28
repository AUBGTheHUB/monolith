import pytest
from result import Ok

from src.database.model.event_registration.participant_model import Participant
from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)
from src.database.mongo.collections.event_registration_collections import (
    PARTICIPANTS_COLLECTION,
)


class FakeCollection:
    def __init__(self):
        self.documents = {}

    async def insert_one(self, document, session=None):
        self.documents[document["_id"]] = document


class FakeDbManager:
    def __init__(self):
        self.collection = FakeCollection()

    def get_collection(self, name):
        assert name == PARTICIPANTS_COLLECTION
        return self.collection


@pytest.mark.asyncio
async def test_create_participant():
    db_manager = FakeDbManager()

    repository = ParticipantsRepository(db_manager=db_manager)

    participant = Participant(
        full_name="Alex Smith",
        age=20,
        email="alex@example.com",
        university="AUBG",
        location="Blagoevgrad",
        share_info_with_sponsors=False,
        game_rank="Gold",
        primary_role="Top",
        alternative_role="Mid",
    )

    result = await repository.create(participant)

    assert isinstance(result, Ok)
    assert result.ok_value.id == participant.id

    stored = db_manager.collection.documents[participant.id]

    assert stored["email"] == "alex@example.com"
    assert stored["primary_role"] == "Top"
    assert stored["alternative_role"] == "Mid"
    assert stored["team_id"] is None
