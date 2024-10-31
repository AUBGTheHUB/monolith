from bson import ObjectId

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


def test_participant_dump_as_json() -> None:
    test_team_id = ObjectId()
    test_participant = Participant(name="Test name", email="test@test.com", is_admin=True, team_id=test_team_id)

    json_data = test_participant.dump_as_json()

    assert json_data["id"] == str(test_participant.id)
    assert json_data["name"] == "Test name"
    assert json_data["email"] == "test@test.com"
    assert json_data["is_admin"] is True
    assert json_data["email_verified"] is False
    assert json_data["team_id"] == str(test_team_id)
    assert json_data["created_at"] == test_participant.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == test_participant.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_participant_dump_as_mongo_db_document() -> None:
    test_team_id = ObjectId()
    test_participant = Participant(name="Test name", email="test@test.com", is_admin=True, team_id=test_team_id)

    mongo_document = test_participant.dump_as_mongo_db_document()

    assert mongo_document["_id"] == test_participant.id
    assert mongo_document["name"] == "Test name"
    assert mongo_document["email"] == "test@test.com"
    assert mongo_document["is_admin"] is True
    assert mongo_document["email_verified"] is False
    assert mongo_document["team_id"] == test_team_id
    assert mongo_document["created_at"] == test_participant.created_at
    assert mongo_document["updated_at"] == test_participant.updated_at


def test_team_dump_as_json() -> None:
    test_team = Team(name="Test Team", is_verified=True)

    json_data = test_team.dump_as_json()

    assert json_data["id"] == str(test_team.id)
    assert json_data["name"] == "Test Team"
    assert json_data["is_verified"] is True
    assert json_data["created_at"] == test_team.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == test_team.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_team_dump_as_mongo_db_document() -> None:
    test_team = Team(name="Test Team", is_verified=True)

    mongo_document = test_team.dump_as_mongo_db_document()

    assert mongo_document["_id"] == test_team.id
    assert mongo_document["name"] == "Test Team"
    assert mongo_document["is_verified"] is True
    assert mongo_document["created_at"] == test_team.created_at
    assert mongo_document["updated_at"] == test_team.updated_at
