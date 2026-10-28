import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.server.routes.registration_routes import register_registration_routes


class FakeRegistrationHandlers:

    async def register_team_admin_handler(self, request):
        return {
            "team_name": request.team_name,
            "email": str(request.participant.email),
        }

    async def register_team_member_handler(
        self,
        request,
        background_tasks,
    ):
        return {
            "team_code": request.team_code,
            "email": str(request.participant.email),
        }

    async def register_solo_handler(self, request):
        return {
            "email": str(request.participant.email),
        }


@pytest.fixture
def client():
    app = FastAPI()

    app.include_router(register_registration_routes(FakeRegistrationHandlers()))

    return TestClient(app)


@pytest.fixture
def participant_data():
    return {
        "full_name": "John Smith",
        "age": 21,
        "email": "john@example.com",
        "university": "AUBG",
        "location": "Blagoevgrad",
        "share_info_with_sponsors": False,
        "game_rank": "Gold",
        "primary_role": "Support",
        "alternative_role": "Mid",
    }


def test_create_team_route(client, participant_data):
    response = client.post(
        "/registration/team/admin",
        json={
            "team_name": "Night Owls",
            "participant": participant_data,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "team_name": "Night Owls",
        "email": "john@example.com",
    }


def test_join_team_route(client, participant_data):
    response = client.post(
        "/registration/team/member",
        json={
            "team_code": "ABC12345",
            "participant": participant_data,
        },
    )

    assert response.status_code == 201
    assert response.json()["team_code"] == "ABC12345"


def test_solo_registration_route(client, participant_data):
    response = client.post(
        "/registration/solo",
        json={"participant": participant_data},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"


def test_invalid_participant_is_rejected(client, participant_data):
    participant_data["email"] = "invalid-email"

    response = client.post(
        "/registration/solo",
        json={"participant": participant_data},
    )

    assert response.status_code == 422


def test_backfill_is_not_public(client):
    response = client.post("/registration/team/backfill")

    assert response.status_code == 404
