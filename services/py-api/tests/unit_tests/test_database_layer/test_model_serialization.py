from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME


def test_participant_dump_as_json(admin_participant_mock: Participant, unverified_team_mock: Team) -> None:

    # When
    json_data = admin_participant_mock.dump_as_json()

    # Then
    assert json_data["id"] == str(admin_participant_mock.id)
    assert json_data["name"] == TEST_USER_NAME
    assert json_data["email"] == TEST_USER_EMAIL
    assert json_data["is_admin"] is True
    assert json_data["email_verified"] is False
    assert json_data["team_id"] == str(unverified_team_mock.id)
    assert json_data["created_at"] == admin_participant_mock.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == admin_participant_mock.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_participant_dump_as_mongo_db_document(admin_participant_mock: Participant, unverified_team_mock: Team) -> None:

    # When
    mongo_document = admin_participant_mock.dump_as_mongo_db_document()

    # Then
    assert mongo_document["_id"] == admin_participant_mock.id
    assert mongo_document["name"] == TEST_USER_NAME
    assert mongo_document["email"] == TEST_USER_EMAIL
    assert mongo_document["is_admin"] is True
    assert mongo_document["email_verified"] is False
    assert mongo_document["team_id"] == unverified_team_mock.id
    assert mongo_document["created_at"] == admin_participant_mock.created_at
    assert mongo_document["updated_at"] == admin_participant_mock.updated_at


def test_team_dump_as_json(unverified_team_mock: Team) -> None:

    # When
    json_data = unverified_team_mock.dump_as_json()

    # Then
    assert json_data["id"] == str(unverified_team_mock.id)
    assert json_data["name"] == TEST_TEAM_NAME
    assert json_data["is_verified"] is False
    assert json_data["created_at"] == unverified_team_mock.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == unverified_team_mock.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_team_dump_as_mongo_db_document(unverified_team_mock: Team) -> None:

    # When
    mongo_document = unverified_team_mock.dump_as_mongo_db_document()

    # Then
    assert mongo_document["_id"] == unverified_team_mock.id
    assert mongo_document["name"] == TEST_TEAM_NAME
    assert mongo_document["is_verified"] is False
    assert mongo_document["created_at"] == unverified_team_mock.created_at
    assert mongo_document["updated_at"] == unverified_team_mock.updated_at
