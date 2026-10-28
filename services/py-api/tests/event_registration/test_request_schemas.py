import pytest
from pydantic import ValidationError

from src.server.schemas.request_schemas.event_registration.schemas import (
    ParticipantInput,
    CreateTeamRequest,
    JoinTeamRequest,
)


VALID_PARTICIPANT = {
    "full_name": "Alex Smith",
    "age": 20,
    "email": "alex@example.com",
    "university": "AUBG",
    "location": "Blagoevgrad",
    "share_info_with_sponsors": False,
    "game_rank": "Gold",
    "primary_role": "Top",
    "alternative_role": "Mid",
}


def test_rejects_negative_age():
    with pytest.raises(ValidationError):
        ParticipantInput(**{**VALID_PARTICIPANT, "age": -5})


def test_rejects_client_admin_flag():
    with pytest.raises(ValidationError):
        ParticipantInput(**{**VALID_PARTICIPANT, "is_team_admin": True})


def test_rejects_blank_team_name():
    with pytest.raises(ValidationError):
        CreateTeamRequest(
            team_name="   ",
            participant=VALID_PARTICIPANT,
        )


def test_joining_requires_team_code():
    with pytest.raises(ValidationError):
        JoinTeamRequest(
            participant=VALID_PARTICIPANT,
        )


def test_sponsor_consent_can_be_false():
    participant = ParticipantInput(**VALID_PARTICIPANT)

    assert participant.share_info_with_sponsors is False
