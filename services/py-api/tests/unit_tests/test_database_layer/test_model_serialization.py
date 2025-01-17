from bson import ObjectId

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME


def test_participant_dump_as_json() -> None:
    test_team_id = ObjectId()
    test_participant = Participant(name=TEST_USER_NAME, email=TEST_USER_EMAIL, is_admin=True, team_id=test_team_id)

    json_data = test_participant.dump_as_json()

    assert json_data["id"] == str(test_participant.id)
    assert json_data["name"] == TEST_USER_NAME
    assert json_data["email"] == TEST_USER_EMAIL
    assert json_data["is_admin"] is True
    assert json_data["email_verified"] is False
    assert json_data["team_id"] == str(test_team_id)
    assert json_data["created_at"] == test_participant.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == test_participant.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_participant_dump_as_mongo_db_document() -> None:
    test_team_id = ObjectId()
    test_participant = Participant(name=TEST_USER_NAME, email=TEST_USER_EMAIL, is_admin=True, team_id=test_team_id)

    mongo_document = test_participant.dump_as_mongo_db_document()

    assert mongo_document["_id"] == test_participant.id
    assert mongo_document["name"] == TEST_USER_NAME
    assert mongo_document["email"] == TEST_USER_EMAIL
    assert mongo_document["is_admin"] is True
    assert mongo_document["email_verified"] is False
    assert mongo_document["team_id"] == test_team_id
    assert mongo_document["created_at"] == test_participant.created_at
    assert mongo_document["updated_at"] == test_participant.updated_at


def test_team_dump_as_json() -> None:
    test_team = Team(name=TEST_TEAM_NAME, is_verified=True)

    json_data = test_team.dump_as_json()

    assert json_data["id"] == str(test_team.id)
    assert json_data["name"] == TEST_TEAM_NAME
    assert json_data["is_verified"] is True
    assert json_data["created_at"] == test_team.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == test_team.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_team_dump_as_mongo_db_document() -> None:
    test_team = Team(name=TEST_TEAM_NAME, is_verified=True)

    mongo_document = test_team.dump_as_mongo_db_document()

    assert mongo_document["_id"] == test_team.id
    assert mongo_document["name"] == TEST_TEAM_NAME
    assert mongo_document["is_verified"] is True
    assert mongo_document["created_at"] == test_team.created_at
    assert mongo_document["updated_at"] == test_team.updated_at
