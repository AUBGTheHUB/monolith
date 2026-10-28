PARTICIPANTS_COLLECTION = "event_registration_participants"
TEAMS_COLLECTION = "event_registration_teams"

from src.database.mongo.db_manager import MongoDatabaseManager


async def ensure_event_registration_indexes(
    db_manager: MongoDatabaseManager,
) -> None:

    participants_collection = db_manager.get_collection(PARTICIPANTS_COLLECTION)

    teams_collection = db_manager.get_collection(TEAMS_COLLECTION)

    await participants_collection.create_index(
        "email",
        unique=True,
    )

    await teams_collection.create_index(
        "code",
        unique=True,
    )
