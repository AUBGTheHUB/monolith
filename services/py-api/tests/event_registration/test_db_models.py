from src.database.model.event_registration.participant_model import Participant
from src.database.model.event_registration.team_model import Team


def make_participant():
    return Participant(
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


def test_participant_stores_role_preferences():
    participant = make_participant()
    document = participant.dump_as_mongo_db_document()

    assert document["primary_role"] == "Top"
    assert document["alternative_role"] == "Mid"
    assert document["team_id"] is None
    assert document["is_team_leader"] is False


def test_team_starts_with_one_member():
    participant = make_participant()

    team = Team(
        name="Team Alpha",
        code="ABC12345",
        leader_id=participant.id,
    )

    document = team.dump_as_mongo_db_document()

    assert document["member_count"] == 1
    assert document["leader_id"] == participant.id
    assert document["completed_at"] is None
    assert document["completion_email_sent_at"] is None


def test_join_code_not_in_public_team_json() -> None:
    participant = make_participant()

    team = Team(
        name="Team Alpha",
        code="ABC12345",
        leader_id=participant.id,
    )

    assert "code" not in team.dump_as_json()
