import pytest
import pytest_asyncio
from asyncio import get_running_loop, new_event_loop, AbstractEventLoop
from httpx import AsyncClient, ASGITransport, Response
from structlog.stdlib import get_logger
from typing import Callable, Dict, Any
from src.server.app_entrypoint import app

LOG = get_logger()

PARTICIPANT_ENDPOINT_URL = "/api/v3/hackathon/participants"
TEAM_ENDPOINT_URL = "/api/v3/hackathon/teams"


# Based on: https://stackoverflow.com/questions/61022713/pytest-asyncio-has-a-closed-event-loop-but-only-when-running-all-tests
# The tests display a deprecation warning. Can be replaced if a better solution is found
@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    try:
        loop = get_running_loop()
    except RuntimeError:
        loop = new_event_loop()
    yield loop
    loop.close()


# The scope is set to session so that that Async Client is only initialized once throughout the testing session,
# instead of initializing it on every test function invocation
# Read More: https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    LOG.debug("Opening Async Client")
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()


# The following is an exapmle of factories as fixtures in pytest
# It manages the creation of participants and ensures the cleanup process after every test function
# You can read more about that: https://docs.pytest.org/en/stable/how-to/fixtures.html#factories-as-fixtures
# It uses the same philosophy for the teardown as it is suggested on the example of the docs above.
# Learn more about fixture teardown here: https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization
@pytest_asyncio.fixture
async def create_test_participant(async_client: AsyncClient) -> Callable[..., Dict[str, Any]]:

    request_results = []

    # Fixtures as factories - Add docs
    async def _create(participant_body: Dict[str, Any]) -> Response:
        LOG.debug("Creating a test participant")
        result = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=participant_body)
        request_results.append(result)
        return result

    yield _create

    LOG.debug("Cleaning up the test participants")
    # Perform clean-up. If we are dealing with an admin participant, we should clean both the participant and the team.
    # Otherwise deleting only the participant is sufficient.
    for result in request_results:
        result_json = result.json()
        if "participant" in result_json:
            PARTICIPANT_ID = result_json["participant"]["id"]
            await async_client.delete(
                url=f"{PARTICIPANT_ENDPOINT_URL}/{PARTICIPANT_ID}", headers={"Authorization": "Bearer OFFLINE_TOKEN"}
            )

            # If a team was created with the participant (admin participant case) clean the team up
            if result_json["team"]:
                TEAM_ID = result_json["team"]["id"]
                await async_client.delete(
                    url=f"{TEAM_ENDPOINT_URL}/{TEAM_ID}", headers={"Authorization": "Bearer OFFLINE_TOKEN"}
                )
