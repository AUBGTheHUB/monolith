from typing import Any, Callable, Dict, Literal
import pytest


def generate_participant_request_body(
    registration_type: Literal["admin", "random", "invite_link"],
    name: str | None = "testtest",
    email: str | None = "testtest@test.com",
    is_admin: bool | None = False,
    **kwargs: Any
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


@pytest.mark.asyncio
async def test_create_random_participant(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    resp = await create_test_participant(participant_body=random_participant_body)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == "testtest"
    assert resp_json["participant"]["email"] == "testtest@test.com"
    assert resp_json["participant"]["is_admin"] is False
    assert resp_json["participant"]["email_verified"] is False
    assert resp_json["participant"]["team_id"] is None
    assert resp_json["team"] is None


@pytest.mark.asyncio
async def test_create_random_participant_email_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    random_participant_body = generate_participant_request_body(registration_type="random", is_admin=None)
    await create_test_participant(participant_body=random_participant_body)
    resp = await create_test_participant(participant_body=random_participant_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_no_team_name(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    is_admin_true_body = generate_participant_request_body(registration_type="admin", is_admin=True)
    resp = await create_test_participant(participant_body=is_admin_true_body)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_random_participant_missing_required_fields(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    missing_req_fields_body = generate_participant_request_body(registration_type="admin", name=None)
    resp = await create_test_participant(participant_body=missing_req_fields_body)
    assert resp.status_code == 422

    resp_json = resp.json()

    assert resp_json["detail"][0]["type"] == "missing"
    assert resp_json["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_admin_participant(create_test_participant: Callable[..., Dict[str, Any]]) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam"
    )
    resp = await create_test_participant(participant_body=admin_participant_body)
    assert resp.status_code == 201

    resp_json = resp.json()

    assert resp_json["participant"]["name"] == "testtest"
    assert resp_json["participant"]["email"] == "testtest@test.com"
    assert resp_json["participant"]["is_admin"] is True
    assert resp_json["participant"]["email_verified"] is False
    assert resp_json["participant"]["team_id"] == resp_json["team"]["id"]
    assert resp_json["team"]["name"] == "testteam"
    assert resp_json["team"]["is_verified"] is False


# The following test shows the order of create operations when adding an admin participant:
# We first create the team --> create the admin
# That is why when trying to create the same admin we get the message that the team already exists.
# We tried to create a team with the same name twice and the app throws an exception in that moment.
@pytest.mark.asyncio
async def test_create_admin_participant_email_and_team_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam"
    )
    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=admin_participant_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_team_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam"
    )
    existing_team_name_body = generate_participant_request_body(
        registration_type="admin", email="testtest1@test.com", is_admin=True, team_name="testteam"
    )

    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=existing_team_name_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Team with this name already exists"


@pytest.mark.asyncio
async def test_create_admin_participant_email_already_exists(
    create_test_participant: Callable[..., Dict[str, Any]]
) -> None:

    admin_participant_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam"
    )
    existing_team_name_body = generate_participant_request_body(
        registration_type="admin", is_admin=True, team_name="testteam1"
    )

    await create_test_participant(participant_body=admin_participant_body)
    resp = await create_test_participant(participant_body=existing_team_name_body)
    assert resp.status_code == 409

    resp_json = resp.json()

    assert resp_json["error"] == "Participant with this email already exists"
