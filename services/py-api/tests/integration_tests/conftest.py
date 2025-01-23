from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport, Response
from structlog.stdlib import get_logger
from typing import AsyncGenerator, Dict, Any, List, Literal, Protocol, Union
from src.app_entrypoint import app
from os import environ

LOG = get_logger()

PARTICIPANT_ENDPOINT_URL = "/api/v3/hackathon/participants"
PARTICIPANT_VERIFY_URL = "/api/v3/hackathon/participants/verify"
TEAM_ENDPOINT_URL = "/api/v3/hackathon/teams"

TEST_USER_NAME = "Test User"
TEST_TEAM_NAME = "Test Team"
TEST_USER_EMAIL = "test@test.com"


# Due to the `async_client` fixture which is persisted across the integration tests session we need to keep all tests
# running in the same event loop, otherwise we get `Event loop is closed`. This is because by default, each test runs
# in a separate event loop (scope=function). Also, it’s highly recommended for neighboring tests to use the same event
# loop scope, and as we use "session" for our async_client we need all integration tests to use "session" as well.
# https://pytest-asyncio.readthedocs.io/en/latest/concepts.html
# https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
# https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html
def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
    pytest_asyncio_tests = (item for item in items if pytest_asyncio.is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


# The scope is set to session so that that Async Client is only initialized once throughout the testing session,
# instead of initializing it on every test function invocation
# Read More: https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    LOG.debug("Opening Async Client")
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    LOG.debug("Closing Async Client")
    await client.aclose()


class CreateTestParticipantCallable(Protocol):
    """
    A callable protocol that represents an asynchronous function to create a test participant.

    This callable takes the following parameters:
    - participant_body: A dictionary containing participant data.
    - jwt_token: An optional JWT token as a string for authentication.

    Returns:
    - An awaitable dictionary containing the participant creation response.
    """

    async def __call__(self, participant_body: Dict[str, Any], jwt_token: Union[str, None] = None) -> Response: ...


@patch.dict(environ, {"SECRET_AUTH_TOKEN": "OFFLINE_TOKEN"})
async def clean_up_test_participant(async_client: AsyncClient, result_json: Dict[str, Any]) -> None:

    participant_id = result_json["participant"]["id"]
    await async_client.delete(
        url=f"{PARTICIPANT_ENDPOINT_URL}/{participant_id}",
        headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
    )

    if result_json["team"] is not None:
        team_id = result_json["team"]["id"]
        await async_client.delete(
            url=f"{TEAM_ENDPOINT_URL}/{team_id}",
            headers={"Authorization": f"Bearer {environ['SECRET_AUTH_TOKEN']}"},
        )


# The following is an exapmle of factories as fixtures in pytest
# It manages the creation of participants and ensures the cleanup process after every test function
# You can read more about that: https://docs.pytest.org/en/stable/how-to/fixtures.html#factories-as-fixtures
# It uses the same philosophy for the teardown as it is suggested on the example of the docs above.
# Learn more about fixture teardown here: https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization


@pytest_asyncio.fixture
async def create_test_participant(async_client: AsyncClient) -> AsyncGenerator[CreateTestParticipantCallable, None]:
    """
    A pytest fixture for managing the lifecycle of test participants in asynchronous tests.

    This fixture provides a callable that allows tests to create participants using the application's API.
    The fixture also ensures proper cleanup after tests, removing any participants or associated data created during the test.

    Parameters:
    - async_client (AsyncClient): An HTTP client instance for making asynchronous API requests.

    Yields:
    - CreateTestParticipantCallable: A callable to create participants. The callable signature is:
      async def(participant_body: Dict[str, Any], jwt_token: Union[str, None] = None) -> Dict[str, Any]

      - participant_body: A dictionary containing the participant's details, such as email and registration type.
      - jwt_token: An optional JWT token as a string to authenticate the request.

    Example Usage:
    ```python
    async def test_create_participant(create_test_participant):
        participant_body = {
            "email": "test@example.com",
            "registration_type": "admin",
            "team_name": "testteam",
        }
        response = await create_test_participant(participant_body)
        assert response["status"] == "success"
    ```

    Cleanup:
    - The fixture automatically deletes any participants created during the test when the test completes.
    - If the participant is an admin, the associated team will also be cleaned up.

    Notes:
    - This fixture is asynchronous and should be used in tests marked with `pytest.mark.asyncio`.
    - It leverages the application's API endpoint to simulate participant creation and cleanup.
    """
    request_results = []

    async def _create(participant_body: Dict[str, Any], jwt_token: Union[str, None] = None) -> Response:
        LOG.debug("Creating a test participant")
        if jwt_token is None:
            result = await async_client.post(PARTICIPANT_ENDPOINT_URL, json=participant_body)
        else:
            result = await async_client.post(f"{PARTICIPANT_ENDPOINT_URL}?jwt_token={jwt_token}", json=participant_body)
        request_results.append(result)
        return result

    yield _create

    for result in request_results:
        if result.status_code == 201:
            LOG.debug("Cleaning up test participant")
            await clean_up_test_participant(async_client=async_client, result_json=result.json())


class ParticipantRequestBodyCallable(Protocol):
    def __call__(
        self,
        registration_type: Literal["admin", "random", "invite_link"],
        name: Union[str, None] = TEST_USER_NAME,
        email: Union[str, None] = TEST_USER_EMAIL,
        is_admin: Union[bool, None] = False,
        **kwargs: Any,
    ) -> Dict[str, Any]: ...


@pytest_asyncio.fixture
def generate_participant_request_body() -> ParticipantRequestBodyCallable:
    def participant_request_body_generator(
        registration_type: Literal["admin", "random", "invite_link"],
        name: Union[str, None] = TEST_USER_NAME,
        email: Union[str, None] = TEST_USER_EMAIL,
        is_admin: Union[bool, None] = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """This method is flexible with generating participant request bodies. To disable a property just call it with
        generate_participant_request_body(email=None) i.e.
        """
        registration_info = {
            "registration_type": registration_type,
            "name": name,
            "email": email,
            "is_admin": is_admin,
            **kwargs,
        }

        cln_reg_info = {key: value for key, value in registration_info.items() if value is not None}
        # A new dict without None values
        return {"registration_info": cln_reg_info}

    return participant_request_body_generator


@pytest.fixture
def mock_obj_id() -> str:
    return "507f1f77bcf86cd799439011"


@pytest.fixture
def thirty_sec_jwt_exp_limit() -> float:
    return (datetime.now(tz=timezone.utc) + timedelta(seconds=30)).timestamp()
