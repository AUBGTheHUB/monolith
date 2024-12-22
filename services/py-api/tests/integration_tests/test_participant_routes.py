from typing import Any, Callable, Dict
import pytest


def generate_participant_request_body(
    name: str | None = "testtest", email: str | None = "testtest@test.com", is_admin: bool | None = False, **kwargs: Any
) -> Dict[str, Any]:

    request_body = {"name": name, "email": email, "is_admin": is_admin, **kwargs}

    # If any of the fields are 'None' - don't include them in the request body
    for key in list(request_body.keys()):  # Convert to list to avoid runtime error while modifying dictionary
        if request_body[key] is None:
            del request_body[key]

    return request_body


@pytest.mark.asyncio
async def test_create_random_participant(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    RANDOM_PARTICIPANT_BODY = generate_participant_request_body()
    resp = await create_test_participant(participant_body=RANDOM_PARTICIPANT_BODY)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == "testtest"
    assert resp_json["participant"]["email"] == "testtest@test.com"
    assert resp_json["participant"]["is_admin"] == False
    assert resp_json["participant"]["email_verified"] == False
    assert resp_json["participant"]["team_id"] == "None"
    assert resp_json["team"] == None


@pytest.mark.asyncio
async def test_create_random_participant_email_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    RANDOM_PARTICIPANT_BODY = generate_participant_request_body()
    await create_test_participant(participant_body=RANDOM_PARTICIPANT_BODY)
    resp = await create_test_participant(participant_body=RANDOM_PARTICIPANT_BODY)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"


@pytest.mark.asyncio
async def test_create_random_participant_is_admin_true(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    IS_ADMIN_TRUE_BODY = generate_participant_request_body(is_admin=True)
    resp = await create_test_participant(participant_body=IS_ADMIN_TRUE_BODY)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["msg"] == "Value error, Field `team_name` is required when `is_admin=True`"


@pytest.mark.asyncio
async def test_create_random_participant_missing_required_fields(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    MISSING_REQ_FIELDS_BODY = generate_participant_request_body(name=None)
    resp = await create_test_participant(participant_body=MISSING_REQ_FIELDS_BODY)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["type"] == "missing"
    assert resp_json["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_admin_participant(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    ADMIN_PARTICIPANT_BODY = generate_participant_request_body(is_admin=True, team_name="testteam")
    resp = await create_test_participant(participant_body=ADMIN_PARTICIPANT_BODY)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == "testtest"
    assert resp_json["participant"]["email"] == "testtest@test.com"
    assert resp_json["participant"]["is_admin"] == True
    assert resp_json["participant"]["email_verified"] == False
    assert resp_json["participant"]["team_id"] == resp_json["team"]["id"]
    assert resp_json["team"]["name"] == "testteam"
    assert resp_json["team"]["is_verified"] == False


# The following test shows the order of create operations when adding an admin participant:
# We first create the team --> create the admin
# That is why when trying to create the same admin we get the message that the team already exists.
# We tried to create a team with the same name twice and the app throws an exception in that moment.
@pytest.mark.asyncio
async def test_create_admin_participant_email_and_team_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    ADMIN_PARTICIPANT_BODY = generate_participant_request_body(is_admin=True, team_name="testteam")
    await create_test_participant(participant_body=ADMIN_PARTICIPANT_BODY)
    resp = await create_test_participant(participant_body=ADMIN_PARTICIPANT_BODY)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_team_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    ADMIN_PARTICIPANT_BODY = generate_participant_request_body(is_admin=True, team_name="testteam")
    EXISTING_TEAM_NAME_BODY = generate_participant_request_body(
        email="testtest1@test.com", is_admin=True, team_name="testteam"
    )

    await create_test_participant(participant_body=ADMIN_PARTICIPANT_BODY)
    resp = await create_test_participant(participant_body=EXISTING_TEAM_NAME_BODY)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_email_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    ADMIN_PARTICIPANT_BODY = generate_participant_request_body(is_admin=True, team_name="testteam")
    EXISTING_TEAM_NAME_BODY = generate_participant_request_body(is_admin=True, team_name="testteam1")

    await create_test_participant(participant_body=ADMIN_PARTICIPANT_BODY)
    resp = await create_test_participant(participant_body=EXISTING_TEAM_NAME_BODY)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"
