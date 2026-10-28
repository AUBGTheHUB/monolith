import pytest

from src.database.mongo.collections.event_registration_collections import (
    PARTICIPANTS_COLLECTION,
    TEAMS_COLLECTION,
    ensure_event_registration_indexes,
)


class FakeCollection:

    def __init__(self):
        self.indexes = []

    async def create_index(self, key, unique=False):
        self.indexes.append(
            {
                "key": key,
                "unique": unique,
            }
        )


class FakeDbManager:

    def __init__(self):
        self.collections = {
            PARTICIPANTS_COLLECTION: FakeCollection(),
            TEAMS_COLLECTION: FakeCollection(),
        }

    def get_collection(self, name):
        return self.collections[name]


@pytest.mark.asyncio
async def test_event_registration_indexes_are_unique():
    db_manager = FakeDbManager()

    await ensure_event_registration_indexes(db_manager)

    participant_indexes = db_manager.collections[PARTICIPANTS_COLLECTION].indexes

    team_indexes = db_manager.collections[TEAMS_COLLECTION].indexes

    assert participant_indexes == [{"key": "email", "unique": True}]

    assert team_indexes == [{"key": "code", "unique": True}]
