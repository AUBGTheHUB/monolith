from src.database.repository.participants_repository import ParticipantsRepository
import pytest
from httpx import AsyncClient
from structlog.stdlib import get_logger

LOG = get_logger()

PARTICIPANT_ENDPOINT_URL = "/api/v3/hackathon/participants"
RANDOM_PARTICIPANT_BODY = {"name": "testtest", "email": "testtest@test.com", "is_admin": False}


@pytest.mark.asyncio(loop_scope="session")
async def test_create_random_participant(
    async_client: AsyncClient, participant_repository: ParticipantsRepository
) -> None:
    resp = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=RANDOM_PARTICIPANT_BODY)

    # Perform cleanup
    # It should be before the assertions so that if one of them fails the cleanup still happens
    await participant_repository.delete(resp.json()["participant"]["id"])

    assert resp.status_code == 201
    assert resp.json()["participant"]["name"] == "testtest"
    assert resp.json()["participant"]["email"] == "testtest@test.com"
    assert resp.json()["participant"]["is_admin"] == False
    assert resp.json()["participant"]["email_verified"] == False
    assert resp.json()["participant"]["team_id"] == "None"
    assert resp.json()["team"] == None
