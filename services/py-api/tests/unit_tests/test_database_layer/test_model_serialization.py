from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from tests.integration_tests.conftest import TEST_TEAM_NAME, TEST_USER_EMAIL, TEST_USER_NAME


def test_participant_dump_as_json(mock_admin_participant: Participant, mock_unverified_team: Team) -> None:

    json_data = mock_admin_participant.dump_as_json()

    assert json_data["id"] == str(mock_admin_participant.id)
    assert json_data["name"] == TEST_USER_NAME
    assert json_data["email"] == TEST_USER_EMAIL
    assert json_data["is_admin"] is True
    assert json_data["email_verified"] is False
    assert json_data["team_id"] == str(mock_unverified_team.id)
    assert json_data["created_at"] == mock_admin_participant.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == mock_admin_participant.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_participant_dump_as_mongo_db_document(mock_admin_participant: Participant, mock_unverified_team: Team) -> None:

    mongo_document = mock_admin_participant.dump_as_mongo_db_document()

    assert mongo_document["_id"] == mock_admin_participant.id
    assert mongo_document["name"] == TEST_USER_NAME
    assert mongo_document["email"] == TEST_USER_EMAIL
    assert mongo_document["is_admin"] is True
    assert mongo_document["email_verified"] is False
    assert mongo_document["team_id"] == mock_unverified_team.id
    assert mongo_document["created_at"] == mock_admin_participant.created_at
    assert mongo_document["updated_at"] == mock_admin_participant.updated_at


def test_team_dump_as_json(mock_unverified_team: Team) -> None:

    json_data = mock_unverified_team.dump_as_json()

    assert json_data["id"] == str(mock_unverified_team.id)
    assert json_data["name"] == TEST_TEAM_NAME
    assert json_data["is_verified"] is False
    assert json_data["created_at"] == mock_unverified_team.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert json_data["updated_at"] == mock_unverified_team.updated_at.strftime("%Y-%m-%d %H:%M:%S")


def test_team_dump_as_mongo_db_document(mock_unverified_team: Team) -> None:

    mongo_document = mock_unverified_team.dump_as_mongo_db_document()

    assert mongo_document["_id"] == mock_unverified_team.id
    assert mongo_document["name"] == TEST_TEAM_NAME
    assert mongo_document["is_verified"] is False
    assert mongo_document["created_at"] == mock_unverified_team.created_at
    assert mongo_document["updated_at"] == mock_unverified_team.updated_at
