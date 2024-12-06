from src.database.repository.participants_repository import ParticipantsRepository
import pytest
from httpx import AsyncClient
from src.database.repository.teams_repository import TeamsRepository

PARTICIPANT_ENDPOINT_URL = "/api/v3/hackathon/participants"

RANDOM_PARTICIPANT_BODY = {"name": "testtest", "email": "testtest@test.com", "is_admin": False}
IS_ADMIN_TRUE_BODY = {"name": "testtest", "email": "testtest@test.com", "is_admin": True}
MISSING_REQ_FIELDS_BODY = {"name": "testtest", "is_admin": False}

ADMIN_PARTICIPANT_BODY = {"name": "testtest", "email": "testtest@test.com", "is_admin": True, "team_name": "testteam"}
EXISTING_TEAM_NAME_BODY = {"name": "testtest", "email": "testtest1@test.com", "is_admin": True, "team_name": "testteam"}
EXISTING_EMAIL_BODY = {"name": "testtest", "email": "testtest@test.com", "is_admin": True, "team_name": "testteam1"}


@pytest.mark.asyncio(loop_scope="session")
async def test_create_random_participant(
    async_client: AsyncClient, participant_repository: ParticipantsRepository
) -> None:
    resp = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=RANDOM_PARTICIPANT_BODY)

    # Perform cleanup
    await participant_repository.delete(resp.json()["participant"]["id"])

    assert resp.status_code == 201
    assert resp.json()["participant"]["name"] == "testtest"
    assert resp.json()["participant"]["email"] == "testtest@test.com"
    assert resp.json()["participant"]["is_admin"] == False
    assert resp.json()["participant"]["email_verified"] == False
    assert resp.json()["participant"]["team_id"] == "None"
    assert resp.json()["team"] == None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_random_participant_email_already_exists(
    async_client: AsyncClient, participant_repository: ParticipantsRepository
) -> None:

    resp1 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=RANDOM_PARTICIPANT_BODY)
    resp2 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=RANDOM_PARTICIPANT_BODY)

    # Performing cleanup, only the first response is successful
    await participant_repository.delete(resp1.json()["participant"]["id"])

    assert resp2.status_code == 409
    assert resp2.json()["error"] == "Participant with this email already exists"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_random_participant_is_admin_true(async_client: AsyncClient) -> None:

    resp = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=IS_ADMIN_TRUE_BODY)

    assert resp.status_code == 422
    assert resp.json()["detail"][0]["msg"] == "Value error, Field `team_name` is required when `is_admin=True`"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_random_participant_missing_required_fields(async_client: AsyncClient) -> None:

    resp = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=MISSING_REQ_FIELDS_BODY)

    assert resp.status_code == 422
    assert resp.json()["detail"][0]["type"] == "missing"
    assert resp.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_admin_participant(
    async_client: AsyncClient, participant_repository: ParticipantsRepository, team_repository: TeamsRepository
) -> None:
    resp = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=ADMIN_PARTICIPANT_BODY)

    """
    >PERFORMING CLEANUP
    The cleanup is done here so that the failing assertions do not interrupt the cleanup process.
    We have saved the state of the request in the resp variable and we can still perform checks on it.
    """
    await participant_repository.delete(resp.json()["participant"]["id"])
    await team_repository.delete(resp.json()["team"]["id"])

    assert resp.status_code == 201
    assert resp.json()["participant"]["name"] == "testtest"
    assert resp.json()["participant"]["email"] == "testtest@test.com"
    assert resp.json()["participant"]["is_admin"] == True
    assert resp.json()["participant"]["email_verified"] == False
    assert resp.json()["participant"]["team_id"] == resp.json()["team"]["id"]
    assert resp.json()["team"]["name"] == "testteam"
    assert resp.json()["team"]["is_verified"] == False


@pytest.mark.asyncio(loop_scope="session")
async def test_create_admin_participant_email_and_team_already_exists(
    async_client: AsyncClient, participant_repository: ParticipantsRepository, team_repository: TeamsRepository
) -> None:

    resp1 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=ADMIN_PARTICIPANT_BODY)
    resp2 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=ADMIN_PARTICIPANT_BODY)

    # Performing cleanup, only the first response is successful
    await participant_repository.delete(resp1.json()["participant"]["id"])
    await team_repository.delete(resp1.json()["team"]["id"])

    assert resp2.status_code == 409
    assert resp2.json()["error"] == "Team with this name already exists"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_admin_participant_team_already_exists(
    async_client: AsyncClient, participant_repository: ParticipantsRepository, team_repository: TeamsRepository
) -> None:

    resp1 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=ADMIN_PARTICIPANT_BODY)
    resp2 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=EXISTING_TEAM_NAME_BODY)

    # Performing cleanup, only the first response is successful
    await participant_repository.delete(resp1.json()["participant"]["id"])
    await team_repository.delete(resp1.json()["team"]["id"])

    assert resp2.status_code == 409
    assert resp2.json()["error"] == "Team with this name already exists"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_admin_participant_email_already_exists(
    async_client: AsyncClient, participant_repository: ParticipantsRepository, team_repository: TeamsRepository
) -> None:

    resp1 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=ADMIN_PARTICIPANT_BODY)
    resp2 = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=EXISTING_EMAIL_BODY)

    # Performing cleanup, only the first response is successful
    await participant_repository.delete(resp1.json()["participant"]["id"])
    await team_repository.delete(resp1.json()["team"]["id"])

    assert resp2.status_code == 409
    assert resp2.json()["error"] == "Participant with this email already exists"
